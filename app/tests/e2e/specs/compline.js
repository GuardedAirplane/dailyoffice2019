/**
 * E2E tests for Compline (US4).
 * 
 * These tests validate that users can successfully view Compline
 * with all its components rendered correctly in the browser.
 * 
 * Test Coverage:
 * - T073-T074: E2E tests for viewing Compline
 */

describe('Compline E2E Tests', () => {
  const baseUrl = Cypress.env('BASE_URL') || 'http://localhost:8080';

  describe('Page Loading', () => {
    it('should load Compline page for a regular day', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/compline`);
      cy.contains('Compline').should('be.visible');
      cy.contains('Monday').should('be.visible');
    });

    it('should load Compline page for a feast day', () => {
      cy.visit(`${baseUrl}/office/2024-12-25/compline`);
      cy.contains('Compline').should('be.visible');
      cy.contains('Christmas').should('be.visible');
    });
  });

  describe('Liturgical Components', () => {
    beforeEach(() => {
      cy.visit(`${baseUrl}/office/2024-01-15/compline`);
    });

    it('should display heading with office name', () => {
      cy.contains('Compline').should('be.visible');
    });

    it('should display commemoration listing', () => {
      cy.get('[data-testid="commemoration-listing"]').should('exist');
    });

    it('should display opening', () => {
      cy.contains('The Lord Almighty grant us a peaceful night').should('be.visible');
    });

    it('should display confession section', () => {
      cy.contains('Confession of Sin').should('be.visible');
    });

    it('should display invitatory', () => {
      cy.contains('Our help is in the Name of the Lord').should('be.visible');
    });

    it('should display psalms section', () => {
      cy.contains('The Psalms').should('be.visible');
    });

    it('should display scripture reading', () => {
      cy.contains('The Lessons').should('be.visible');
    });

    it('should display prayers section', () => {
      cy.contains('The Prayers').should('be.visible');
    });

    it('should display Nunc Dimittis canticle', () => {
      cy.contains('The Song of Simeon').should('be.visible');
    });

    it('should display conclusion', () => {
      cy.contains('Guide us waking, O Lord').should('be.visible');
    });
  });

  describe('Component Order', () => {
    it('should render components in correct liturgical order', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/compline`);

      const expectedOrder = [
        'Compline',
        'Opening',
        'Confession',
        'Invitatory',
        'Psalms',
        'Lessons',
        'Prayers',
        'Song of Simeon',
        'Conclusion'
      ];

      cy.get('.office-module').then(($modules) => {
        expectedOrder.forEach((text, index) => {
          if (index < $modules.length) {
            cy.wrap($modules[index]).should('contain', text);
          }
        });
      });
    });
  });

  describe('Scripture Rotation', () => {
    it('should use Jeremiah 14:9 on Monday', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/compline`); // Monday
      cy.contains('JEREMIAH 14:9').should('be.visible');
    });

    it('should use Matthew 11:28-30 on Tuesday', () => {
      cy.visit(`${baseUrl}/office/2024-01-16/compline`); // Tuesday
      cy.contains('MATTHEW 11:28-30').should('be.visible');
    });

    it('should use Hebrews 13:20-21 on Wednesday', () => {
      cy.visit(`${baseUrl}/office/2024-01-17/compline`); // Wednesday
      cy.contains('HEBREWS 13:20-21').should('be.visible');
    });

    it('should use 1 Peter 5:8-9 on Thursday', () => {
      cy.visit(`${baseUrl}/office/2024-01-18/compline`); // Thursday
      cy.contains('1 PETER 5:8-9').should('be.visible');
    });
  });

  describe('Fixed Psalms', () => {
    it('should always display fixed psalms (4, 31, 91, 134)', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/compline`);
      
      cy.contains('Psalm 4').should('be.visible');
      cy.contains('Psalm 31').should('be.visible');
      cy.contains('Psalm 91').should('be.visible');
      cy.contains('Psalm 134').should('be.visible');
    });
  });

  describe('Seasonal Variations', () => {
    it('should omit Alleluia during Lent in invitatory', () => {
      cy.visit(`${baseUrl}/office/2024-03-15/compline`); // Lent
      cy.get('[data-testid="invitatory"]').within(() => {
        cy.contains('Alleluia').should('not.exist');
      });
    });

    it('should include Alleluia in canticle during Easter', () => {
      cy.visit(`${baseUrl}/office/2024-04-15/compline`); // Eastertide
      cy.get('[data-testid="canticle"]').within(() => {
        cy.contains('Alleluia').should('be.visible');
      });
    });

    it('should include Alleluia in conclusion during Easter', () => {
      cy.visit(`${baseUrl}/office/2024-04-15/compline`); // Eastertide
      cy.get('[data-testid="conclusion"]').within(() => {
        cy.contains('Alleluia').should('be.visible');
      });
    });
  });

  describe('Feast Days', () => {
    it('should display Christmas in heading', () => {
      cy.visit(`${baseUrl}/office/2024-12-25/compline`);
      cy.contains('Christmas').should('be.visible');
    });

    it('should display Easter in heading', () => {
      cy.visit(`${baseUrl}/office/2024-03-31/compline`);
      cy.contains('Easter').should('be.visible');
    });
  });

  describe('Nunc Dimittis Canticle', () => {
    it('should display Nunc Dimittis heading', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/compline`);
      cy.contains('The Song of Simeon').should('be.visible');
    });

    it('should display Nunc Dimittis text', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/compline`);
      cy.contains('Lord, now lettest thou thy servant depart in peace').should('be.visible');
    });

    it('should include Alleluia in Nunc Dimittis during Easter', () => {
      cy.visit(`${baseUrl}/office/2024-04-15/compline`); // Eastertide
      cy.contains('The Song of Simeon').parent().within(() => {
        cy.contains('Alleluia').should('be.visible');
      });
    });
  });

  describe('Weekday Collect Rotation', () => {
    it('should display three collects on regular days', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/compline`); // Monday
      cy.get('[data-testid="prayers"]').within(() => {
        cy.get('.collect').should('have.length', 3);
      });
    });

    it('should include Paschal mystery collect on Saturday', () => {
      cy.visit(`${baseUrl}/office/2024-01-20/compline`); // Saturday
      cy.contains('Paschal mystery').should('be.visible');
    });
  });

  describe('Navigation', () => {
    it('should navigate between dates using date picker', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/compline`);
      cy.get('[data-testid="date-picker"]').clear().type('2024-01-16');
      cy.contains('Tuesday').should('be.visible');
    });

    it('should navigate to previous day', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/compline`);
      cy.get('[data-testid="previous-day"]').click();
      cy.url().should('include', '2024-01-14');
    });

    it('should navigate to next day', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/compline`);
      cy.get('[data-testid="next-day"]').click();
      cy.url().should('include', '2024-01-16');
    });

    it('should navigate to different office types', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/compline`);
      cy.get('[data-testid="office-selector"]').select('Morning Prayer');
      cy.url().should('include', 'morning-prayer');
    });
  });

  describe('Error Handling', () => {
    it('should handle invalid dates gracefully', () => {
      cy.visit(`${baseUrl}/office/2024-13-45/compline`, { failOnStatusCode: false });
      cy.contains('Invalid date').should('be.visible');
    });

    it('should handle dates outside supported range', () => {
      cy.visit(`${baseUrl}/office/2030-01-15/compline`, { failOnStatusCode: false });
      cy.contains('Date out of range').should('be.visible');
    });
  });

  describe('Evening Commemorations', () => {
    it('should display evening commemorations', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/compline`);
      cy.get('[data-testid="commemoration-listing"]').should('exist');
      cy.get('[data-testid="commemoration-listing"]').should('have.attr', 'data-evening', 'true');
    });
  });

  describe('Time Window', () => {
    it('should indicate Compline is for evening use', () => {
      cy.visit(`${baseUrl}/office/2024-01-15/compline`);
      cy.contains('night').should('be.visible'); // "peaceful night"
    });
  });

  describe('Responsive Design', () => {
    it('should display correctly on mobile viewport', () => {
      cy.viewport('iphone-6');
      cy.visit(`${baseUrl}/office/2024-01-15/compline`);
      cy.contains('Compline').should('be.visible');
    });

    it('should display correctly on tablet viewport', () => {
      cy.viewport('ipad-2');
      cy.visit(`${baseUrl}/office/2024-01-15/compline`);
      cy.contains('Compline').should('be.visible');
    });

    it('should display correctly on desktop viewport', () => {
      cy.viewport(1920, 1080);
      cy.visit(`${baseUrl}/office/2024-01-15/compline`);
      cy.contains('Compline').should('be.visible');
    });
  });
});
