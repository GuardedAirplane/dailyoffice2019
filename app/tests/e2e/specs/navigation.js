/**
 * E2E tests for office navigation (US5).
 * 
 * These tests validate that users can successfully navigate between
 * different office types while preserving the date correctly.
 * 
 * Test Coverage:
 * - T080-T082: E2E tests for navigation between offices
 */

describe('Office Navigation E2E Tests', () => {
  const baseUrl = Cypress.env('BASE_URL') || 'http://localhost:8080';

  describe('Navigation Between Office Types', () => {
    it('should navigate from Morning Prayer to Evening Prayer', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/morning-prayer`);
      cy.contains('Morning Prayer').should('be.visible');
      
      cy.get('[data-testid="office-selector"]').select('Evening Prayer');
      
      cy.url().should('include', '2024-01-15');
      cy.url().should('include', 'evening-prayer');
      cy.contains('Evening Prayer').should('be.visible');
    });

    it('should navigate from Evening Prayer to Midday Prayer', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/evening-prayer`);
      cy.contains('Evening Prayer').should('be.visible');
      
      cy.get('[data-testid="office-selector"]').select('Midday Prayer');
      
      cy.url().should('include', '2024-01-15');
      cy.url().should('include', 'midday-prayer');
      cy.contains('Midday Prayer').should('be.visible');
    });

    it('should navigate from Midday Prayer to Compline', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/midday-prayer`);
      cy.contains('Midday Prayer').should('be.visible');
      
      cy.get('[data-testid="office-selector"]').select('Compline');
      
      cy.url().should('include', '2024-01-15');
      cy.url().should('include', 'compline');
      cy.contains('Compline').should('be.visible');
    });

    it('should navigate from Compline to Morning Prayer', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/compline`);
      cy.contains('Compline').should('be.visible');
      
      cy.get('[data-testid="office-selector"]').select('Morning Prayer');
      
      cy.url().should('include', '2024-01-15');
      cy.url().should('include', 'morning-prayer');
      cy.contains('Morning Prayer').should('be.visible');
    });
  });

  describe('Date Preservation Across Office Types', () => {
    it('should preserve date when switching from Morning to Evening Prayer', () => {
      cy.visit(`${baseUrl}/office/2024-12-25/morning-prayer`);
      cy.contains('December 25, 2024').should('be.visible');
      
      cy.get('[data-testid="office-nav-evening"]').click();
      
      cy.url().should('include', '2024-12-25');
      cy.contains('December 25, 2024').should('be.visible');
    });

    it('should preserve date when switching from Evening to Midday Prayer', () => {
      cy.visit(`${baseUrl}/office/2024-03-31/evening-prayer`);  // Easter
      cy.contains('March 31, 2024').should('be.visible');
      
      cy.get('[data-testid="office-nav-midday"]').click();
      
      cy.url().should('include', '2024-03-31');
      cy.contains('March 31, 2024').should('be.visible');
    });

    it('should preserve date when switching from Midday to Compline', () => {
      cy.visit(`${baseUrl}/office/2024-01-06/midday-prayer`);  // Epiphany
      cy.contains('January 6, 2024').should('be.visible');
      
      cy.get('[data-testid="office-nav-compline"]').click();
      
      cy.url().should('include', '2024-01-06');
      cy.contains('January 6, 2024').should('be.visible');
    });
  });

  describe('Date Navigation', () => {
    it('should navigate to previous day and maintain office type', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/morning-prayer`);
      
      cy.get('[data-testid="previous-day"]').click();
      
      cy.url().should('include', '2024-01-14');
      cy.url().should('include', 'morning-prayer');
      cy.contains('Sunday').should('be.visible');  // Jan 14 is Sunday
    });

    it('should navigate to next day and maintain office type', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/evening-prayer`);
      
      cy.get('[data-testid="next-day"]').click();
      
      cy.url().should('include', '2024-01-16');
      cy.url().should('include', 'evening-prayer');
      cy.contains('Tuesday').should('be.visible');  // Jan 16 is Tuesday
    });

    it('should navigate across month boundaries', () => {
      cy.visit(`${baseUrl}/office/2024-01-31/midday-prayer`);
      
      cy.get('[data-testid="next-day"]').click();
      
      cy.url().should('include', '2024-02-01');
      cy.url().should('include', 'midday-prayer');
      cy.contains('February 1, 2024').should('be.visible');
    });

    it('should navigate across year boundaries', () => {
      cy.visit(`${baseUrl}/office/2024-12-31/compline`);
      
      cy.get('[data-testid="next-day"]').click();
      
      cy.url().should('include', '2025-01-01');
      cy.url().should('include', 'compline');
      cy.contains('January 1, 2025').should('be.visible');
    });
  });

  describe('Navigation Controls', () => {
    it('should display all office navigation links', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/morning-prayer`);
      
      cy.get('[data-testid="office-nav"]').within(() => {
        cy.contains('Morning').should('be.visible');
        cy.contains('Midday').should('be.visible');
        cy.contains('Evening').should('be.visible');
        cy.contains('Compline').should('be.visible');
      });
    });

    it('should highlight current office in navigation', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/morning-prayer`);
      
      cy.get('[data-testid="office-nav-morning"]').should('have.class', 'active');
    });

    it('should display date navigation controls', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/evening-prayer`);
      
      cy.get('[data-testid="date-nav"]').within(() => {
        cy.get('[data-testid="previous-day"]').should('be.visible');
        cy.get('[data-testid="next-day"]').should('be.visible');
        cy.get('[data-testid="date-picker"]').should('be.visible');
      });
    });

    it('should allow direct date input via date picker', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/morning-prayer`);
      
      cy.get('[data-testid="date-picker"]').clear().type('2024-03-31{enter}');
      
      cy.url().should('include', '2024-03-31');
      cy.url().should('include', 'morning-prayer');
      cy.contains('Easter').should('be.visible');
    });
  });

  describe('Keyboard Navigation', () => {
    it('should support arrow key navigation between dates', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/morning-prayer`);
      
      cy.get('body').type('{leftarrow}');
      cy.url().should('include', '2024-01-14');
      
      cy.get('body').type('{rightarrow}');
      cy.url().should('include', '2024-01-15');
    });

    it('should support tab navigation between office types', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/morning-prayer`);
      
      cy.get('[data-testid="office-nav-morning"]').tab();
      cy.focused().should('have.attr', 'data-testid', 'office-nav-midday');
    });
  });

  describe('URL Direct Access', () => {
    it('should support direct URL access to any office and date', () => {
      cy.visit(`${baseUrl}/office/2024-12-25/evening-prayer`);
      
      cy.contains('Evening Prayer').should('be.visible');
      cy.contains('December 25, 2024').should('be.visible');
      cy.contains('Christmas').should('be.visible');
    });

    it('should handle invalid dates gracefully', () => {
      cy.visit(`${baseUrl}/office/2024-13-40/morning-prayer`, { failOnStatusCode: false });
      
      cy.contains('Invalid date').should('be.visible');
    });

    it('should handle invalid office types gracefully', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/invalid-prayer`, { failOnStatusCode: false });
      
      cy.contains('Not found').should('be.visible');
    });
  });

  describe('Office Type Cycling', () => {
    it('should cycle through all four office types in order', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/morning-prayer`);
      
      cy.get('[data-testid="office-nav-midday"]').click();
      cy.url().should('include', 'midday-prayer');
      
      cy.get('[data-testid="office-nav-evening"]').click();
      cy.url().should('include', 'evening-prayer');
      
      cy.get('[data-testid="office-nav-compline"]').click();
      cy.url().should('include', 'compline');
      
      cy.get('[data-testid="office-nav-morning"]').click();
      cy.url().should('include', 'morning-prayer');
    });
  });

  describe('Family Office Navigation', () => {
    it('should navigate to family prayer offices', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/morning-prayer`);
      
      cy.get('[data-testid="family-office-toggle"]').click();
      cy.get('[data-testid="office-nav-family-morning"]').click();
      
      cy.url().should('include', '2024-01-15');
      cy.url().should('include', 'family-morning-prayer');
      cy.contains('Family Morning Prayer').should('be.visible');
    });

    it('should preserve date when switching to family offices', () => {
      cy.visit(`${baseUrl}/office/2024-12-25/evening-prayer`);
      
      cy.get('[data-testid="family-office-toggle"]').click();
      cy.get('[data-testid="office-nav-family-evening"]').click();
      
      cy.url().should('include', '2024-12-25');
      cy.contains('December 25, 2024').should('be.visible');
    });
  });

  describe('Mobile Navigation', () => {
    beforeEach(() => {
      cy.viewport('iphone-6');
    });

    it('should display mobile-friendly navigation menu', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/morning-prayer`);
      
      cy.get('[data-testid="mobile-menu-toggle"]').click();
      cy.get('[data-testid="mobile-office-nav"]').should('be.visible');
    });

    it('should support touch gestures for date navigation', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/evening-prayer`);
      
      cy.get('[data-testid="office-content"]').trigger('swipeleft');
      cy.url().should('include', '2024-01-16');
      
      cy.get('[data-testid="office-content"]').trigger('swiperight');
      cy.url().should('include', '2024-01-15');
    });
  });

  describe('Browser History Integration', () => {
    it('should support browser back button', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/morning-prayer`);
      cy.get('[data-testid="office-nav-evening"]').click();
      
      cy.go('back');
      
      cy.url().should('include', 'morning-prayer');
      cy.contains('Morning Prayer').should('be.visible');
    });

    it('should support browser forward button', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/morning-prayer`);
      cy.get('[data-testid="office-nav-evening"]').click();
      cy.go('back');
      
      cy.go('forward');
      
      cy.url().should('include', 'evening-prayer');
      cy.contains('Evening Prayer').should('be.visible');
    });
  });

  describe('Responsive Navigation Labels', () => {
    it('should show abbreviated labels on small screens', () => {
      cy.viewport(320, 568);  // iPhone SE
      cy.visit(`${baseUrl}/office/2024-01-15/morning-prayer`);
      
      cy.get('[data-testid="office-nav"]').within(() => {
        cy.contains('MP').should('be.visible');  // Abbreviated Morning Prayer
      });
    });

    it('should show full labels on large screens', () => {
      cy.viewport(1920, 1080);
      cy.visit(`${baseUrl}/office/2024-01-15/morning-prayer`);
      
      cy.get('[data-testid="office-nav"]').within(() => {
        cy.contains('Morning Prayer').should('be.visible');
      });
    });
  });
});
