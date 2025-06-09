import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, ActivatedRoute, RouterLink } from '@angular/router';
import { ImmigrationService, ImmigrationRecord } from '../../../services/immigration.service';

@Component({
  selector: 'app-immigration-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './immigration-form.component.html',
  styleUrl: './immigration-form.component.css'
})
export class ImmigrationFormComponent implements OnInit {
  recordForm: FormGroup;
  isEditMode = false;
  recordId: number | null = null;
  loading = false;
  submitted = false;
  errorMessage = '';

  entryTypeOptions = [
    { value: 'ENTRY', label: 'Nhập cảnh' },
    { value: 'EXIT', label: 'Xuất cảnh' }
  ];

  purposeOptions = [
    { value: 'TOURISM', label: 'Du lịch' },
    { value: 'BUSINESS', label: 'Công việc' },
    { value: 'STUDY', label: 'Học tập' },
    { value: 'VISIT', label: 'Thăm thân' },
    { value: 'DIPLOMATIC', label: 'Ngoại giao' },
    { value: 'OTHER', label: 'Khác' }
  ];

  statusOptions = [
    { value: 'PENDING', label: 'Đang xử lý' },
    { value: 'APPROVED', label: 'Đã duyệt' },
    { value: 'REJECTED', label: 'Từ chối' }
  ];

  constructor(
    private formBuilder: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
    private immigrationService: ImmigrationService
  ) {
    this.recordForm = this.formBuilder.group({
      full_name: ['', [Validators.required]],
      date_of_birth: ['', [Validators.required]],
      gender: ['', [Validators.required]],
      nationality: ['', [Validators.required]],
      passport_number: ['', [Validators.required]],
      passport_expiry_date: ['', [Validators.required]],
      entry_type: ['ENTRY', [Validators.required]],
      purpose: ['', [Validators.required]],
      purpose_detail: [''],
      flight_number: ['', [Validators.required]],
      airline: ['', [Validators.required]],
      status: ['PENDING'],
      visa_number: [''],
      address_in_country: [''],
      contact_phone: ['']
    });
  }

  ngOnInit(): void {
    this.recordId = this.route.snapshot.params['id'];
    this.isEditMode = !!this.recordId;

    if (this.isEditMode) {
      this.loading = true;
      this.immigrationService.getRecordById(this.recordId!)
        .subscribe({
          next: (record) => {
            // Format dates for input type="date"
            const formattedRecord = {
              ...record,
              date_of_birth: this.formatDateForInput(record.date_of_birth),
              passport_expiry_date: this.formatDateForInput(record.passport_expiry_date)
            };
            this.recordForm.patchValue(formattedRecord);
            this.loading = false;
          },
          error: (error) => {
            console.error('Error fetching record:', error);
            this.errorMessage = 'Không thể tải thông tin bản ghi. Vui lòng thử lại sau.';
            this.loading = false;
          }
        });
    }
  }

  formatDateForInput(dateString: string): string {
    const date = new Date(dateString);
    return date.toISOString().split('T')[0];
  }

  onSubmit(): void {
    this.submitted = true;

    // Stop if form is invalid
    if (this.recordForm.invalid) {
      return;
    }

    this.loading = true;
    const recordData = {...this.recordForm.value};
    
    // Format dates properly for the backend
    if (recordData.date_of_birth) {
      recordData.date_of_birth = this.formatDateForBackend(recordData.date_of_birth);
    }
    if (recordData.passport_expiry_date) {
      recordData.passport_expiry_date = this.formatDateForBackend(recordData.passport_expiry_date);
    }
    
    console.log('Sending data to backend:', recordData);

    if (this.isEditMode) {
      this.immigrationService.updateRecord(this.recordId!, recordData)
        .subscribe({
          next: () => {
            this.router.navigate(['/records']);
          },
          error: (error) => {
            console.error('Error updating record:', error);
            this.errorMessage = this.getErrorMessage(error);
            this.loading = false;
          }
        });
    } else {
      this.immigrationService.createRecord(recordData)
        .subscribe({
          next: () => {
            this.router.navigate(['/records']);
          },
          error: (error) => {
            console.error('Error creating record:', error);
            this.errorMessage = this.getErrorMessage(error);
            this.loading = false;
          }
        });
    }
  }
  
  formatDateForBackend(dateString: string): string {
    // Convert from YYYY-MM-DD to YYYY-MM-DD format (for backend)
    return dateString;
  }

  getErrorMessage(error: any): string {
    if (error.error) {
      // Trường hợp lỗi validation từ backend
      const errorObj = error.error;
      
      // Xử lý lỗi non_field_errors
      if (errorObj.non_field_errors) {
        return errorObj.non_field_errors.join(', ');
      }
      
      // Chỉ hiển thị giá trị lỗi đầu tiên tìm thấy, không hiển thị tên trường
      for (const field in errorObj) {
        if (errorObj.hasOwnProperty(field) && errorObj[field].length > 0) {
          return errorObj[field][0];
        }
      }
    }
    
    return 'Không thể tạo bản ghi mới. Vui lòng thử lại sau.';
  }
}
