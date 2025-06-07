import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ImmigrationService, ImmigrationRecord } from '../../../services/immigration.service';

@Component({
  selector: 'app-immigration-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './immigration-detail.component.html',
  styleUrl: './immigration-detail.component.css'
})
export class ImmigrationDetailComponent implements OnInit {
  recordId: number = 0;
  record: ImmigrationRecord | null = null;
  loading: boolean = true;
  error: string = '';

  constructor(
    private route: ActivatedRoute,
    private immigrationService: ImmigrationService
  ) {}

  ngOnInit(): void {
    this.recordId = Number(this.route.snapshot.paramMap.get('id'));
    this.loadRecord();
  }

  loadRecord(): void {
    this.loading = true;
    this.immigrationService.getRecordById(this.recordId)
      .subscribe({
        next: (data) => {
          this.record = data;
          this.loading = false;
        },
        error: (error) => {
          console.error('Error loading record:', error);
          this.error = 'Không thể tải thông tin bản ghi. Vui lòng thử lại sau.';
          this.loading = false;
        }
      });
  }
}
