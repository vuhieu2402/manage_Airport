import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ImmigrationService, ImmigrationRecord, ImmigrationResponse } from '../../../services/immigration.service';

@Component({
  selector: 'app-immigration-list',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  templateUrl: './immigration-list.component.html',
  styleUrl: './immigration-list.component.css'
})
export class ImmigrationListComponent implements OnInit {
  records: ImmigrationRecord[] = [];
  loading = false;
  error = '';
  currentPage = 1;
  totalRecords = 0;
  totalPages = 0;
  searchTerm = '';
  Math = Math; // Make Math available in the template

  constructor(private immigrationService: ImmigrationService) { }

  ngOnInit(): void {
    this.loadRecords();
  }

  loadRecords(): void {
    console.log('Loading records for page:', this.currentPage);
    this.loading = true;
    this.error = '';

    this.immigrationService.getRecords(this.currentPage, this.searchTerm)
      .subscribe({
        next: (response: ImmigrationResponse) => {
          console.log('Received response:', response);
          this.records = response.results;
          this.totalRecords = response.count;
          this.totalPages = Math.ceil(response.count / 5); // 5 là số bản ghi mỗi trang
          console.log('Updated state:', {
            recordsCount: this.records.length,
            totalRecords: this.totalRecords,
            totalPages: this.totalPages,
            currentPage: this.currentPage
          });
          this.loading = false;
        },
        error: (err) => {
          console.error('Error loading records:', err);
          this.error = 'Không thể tải dữ liệu. Vui lòng thử lại sau.';
          this.loading = false;
        }
      });
  }

  search(): void {
    console.log('Searching with term:', this.searchTerm);
    this.currentPage = 1; // Reset về trang đầu tiên khi tìm kiếm
    this.loadRecords();
  }

  nextPage(): void {
    console.log('Attempting to go to next page. Current:', this.currentPage, 'Total:', this.totalPages);
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
      console.log('Moving to page:', this.currentPage);
      this.loadRecords();
    }
  }

  prevPage(): void {
    console.log('Attempting to go to previous page. Current:', this.currentPage);
    if (this.currentPage > 1) {
      this.currentPage--;
      console.log('Moving to page:', this.currentPage);
      this.loadRecords();
    }
  }

  deleteRecord(id: number): void {
    if (confirm('Bạn có chắc chắn muốn xóa bản ghi này?')) {
      this.immigrationService.deleteRecord(id)
        .subscribe({
          next: () => {
            this.records = this.records.filter(record => record.id !== id);
            // Nếu trang hiện tại không còn bản ghi nào và không phải trang đầu tiên
            if (this.records.length === 0 && this.currentPage > 1) {
              this.currentPage--;
            }
            this.loadRecords(); // Tải lại danh sách sau khi xóa
          },
          error: (error) => {
            console.error('Error deleting record:', error);
            this.error = 'Không thể xóa bản ghi. Vui lòng thử lại sau.';
          }
        });
    }
  }
}
