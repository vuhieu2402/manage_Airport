import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImmigrationDetailComponent } from './immigration-detail.component';

describe('ImmigrationDetailComponent', () => {
  let component: ImmigrationDetailComponent;
  let fixture: ComponentFixture<ImmigrationDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ImmigrationDetailComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ImmigrationDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
