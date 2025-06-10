import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface ImmigrationRecord {
  id: number;
  full_name: string;
  date_of_birth: string;
  gender: string;
  gender_display?: string;
  nationality: string;
  passport_number: string;
  passport_expiry_date: string;
  entry_type: string;
  entry_type_display?: string;
  purpose: string;
  purpose_display?: string;
  purpose_detail?: string;
  flight_number: string;
  airline: string;
  date_of_entry_exit: string;
  status: string;
  status_display?: string;
  visa_number?: string;
  address_in_country?: string;
  contact_phone?: string;
  created_at: string;
  updated_at: string;
}

export interface ImmigrationResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: ImmigrationRecord[];
}

export interface ImmigrationStatistics {
  total: number;
  by_entry_type: {
    entry: number;
    exit: number;
  };
  by_purpose: {
    [key: string]: number;
  };
  by_status: {
    [key: string]: number;
  };
}

@Injectable({
  providedIn: 'root'
})
export class ImmigrationService {
  private apiUrl = environment.apiUrl;
  
  constructor(private http: HttpClient) { }
  
  getRecords(page: number = 1, search: string = ''): Observable<ImmigrationResponse> {

    
    const body = {
      page: page,
      search: search,
      filters: {}
    };
    

    return this.http.post<ImmigrationResponse>(`${this.apiUrl}/list/`, body);
  }
  
  getRecordById(id: number): Observable<ImmigrationRecord> {
    return this.http.post<ImmigrationRecord>(`${this.apiUrl}/detail/`, { id });
  }
  
  createRecord(record: Partial<ImmigrationRecord>): Observable<ImmigrationRecord> {
    return this.http.post<ImmigrationRecord>(`${this.apiUrl}/create/`, record);
  }
  
  updateRecord(id: number, record: Partial<ImmigrationRecord>): Observable<ImmigrationRecord> {
    return this.http.post<ImmigrationRecord>(`${this.apiUrl}/update/`, { ...record, id });
  }
  
  deleteRecord(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/delete/`, { id });
  }
  
  getStatistics(): Observable<ImmigrationStatistics> {
    return this.http.post<ImmigrationStatistics>(`${this.apiUrl}/statistics/`, {});
  }
}
