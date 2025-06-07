import { TestBed } from '@angular/core/testing';

import { ImmigrationService } from './immigration.service';

describe('ImmigrationService', () => {
  let service: ImmigrationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ImmigrationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
