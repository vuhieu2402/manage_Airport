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
    this.loading = true;
    this.immigrationService.getRecords(this.currentPage, this.searchTerm)
      .subscribe({
        next: (response: ImmigrationResponse) => {
          this.records = response.results;
          this.totalRecords = response.count;
          this.totalPages = Math.ceil(response.count / 5); // 5 là số bản ghi mỗi trang
          this.loading = false;
        },
        error: (err) => {
          this.error = 'Không thể tải dữ liệu. Vui lòng thử lại sau.';
          this.loading = false;
          console.error('Error loading records:', err);
        }
      });
  }

  search(): void {
    this.currentPage = 1; // Reset về trang đầu tiên khi tìm kiếm
    this.loadRecords();
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
      this.loadRecords();
    }
  }

  prevPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.loadRecords();
    }
  }

  deleteRecord(id: number): void {
    if (confirm('Bạn có chắc chắn muốn xóa bản ghi này?')) {
      this.immigrationService.deleteRecord(id).subscribe({
        next: () => {
          this.records = this.records.filter(record => record.id !== id);
          alert('Xóa bản ghi thành công');
        },
        error: (err) => {
          alert('Không thể xóa bản ghi. Vui lòng thử lại sau.');
          console.error('Error deleting record:', err);
        }
      });
    }
  }
}
