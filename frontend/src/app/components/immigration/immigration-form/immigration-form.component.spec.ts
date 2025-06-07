import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImmigrationFormComponent } from './immigration-form.component';

describe('ImmigrationFormComponent', () => {
  let component: ImmigrationFormComponent;
  let fixture: ComponentFixture<ImmigrationFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ImmigrationFormComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ImmigrationFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
