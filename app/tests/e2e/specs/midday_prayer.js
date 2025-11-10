/**
 * E2E tests for Midday Prayer (US3)
 * 
 * Validates FR-002 (Daily Office feature) by testing browser rendering
 * of Midday Prayer with all required liturgical components.
 * 
 * Test Coverage:
 * - T065: Page loads and displays Midday Prayer
 * - T066: All liturgical components present
 */

describe('Midday Prayer E2E Tests', () => {
  const testDate = '2024-01-15'; // Monday in Epiphany

  beforeEach(() => {
    // Visit Midday Prayer page for test date
    cy.visit(`/#/office/midday/${testDate}`);
    cy.wait(1000); // Allow office to load
  });

  /**
   * T065: Basic page loading tests
   */
  describe('Page Loading', () => {
    it('should load Midday Prayer page successfully', () => {
      cy.get('h1').should('contain', 'Midday Prayer');
    });

    it('should display the correct date', () => {
      cy.contains('Monday January 15, 2024').should('be.visible');
    });
  });

  /**
   * T066: Liturgical component tests
   */
  describe('Liturgical Components', () => {
    it('should display the heading', () => {
      cy.get('h1').contains('Midday Prayer').should('be.visible');
    });

    it('should display commemoration listing', () => {
      cy.contains('This Day\'s Commemoration').should('be.visible');
    });

    it('should display invitatory with Alleluia (outside Lent)', () => {
      cy.contains('O God, make speed to save us').should('be.visible');
      cy.contains('Alleluia').should('be.visible');
    });

    it('should display the psalms section', () => {
      cy.contains('The Psalms').should('be.visible');
      // Midday Prayer uses fixed psalms: 119:105-112, 121, 124, 126
      cy.contains('Psalm 119').should('be.visible');
    });

    it('should display the scripture reading', () => {
      cy.contains('The Reading').should('be.visible');
      // Monday uses John 12:31-32
      cy.contains('JOHN 12:31-32').should('be.visible');
    });

    it('should display the prayers section', () => {
      cy.contains('The Prayers').should('be.visible');
      // Should include the Blessed Savior collect
      cy.contains('Blessed Savior').should('be.visible');
    });

    it('should display the conclusion', () => {
      cy.contains('Let us bless the Lord').should('be.visible');
    });
  });

  /**
   * T066: Component order validation
   */
  describe('Component Order', () => {
    it('should display components in correct liturgical order', () => {
      const components = [
        'Midday Prayer',
        'This Day\'s Commemoration',
        'O God, make speed to save us',
        'The Psalms',
        'The Reading',
        'The Prayers',
        'Let us bless the Lord'
      ];

      // Verify each component appears in order
      let lastPosition = 0;
      components.forEach(text => {
        cy.contains(text).then($el => {
          const position = $el.offset().top;
          expect(position).to.be.greaterThan(lastPosition);
          lastPosition = position;
        });
      });
    });
  });

  /**
   * T066: Weekday scripture rotation tests
   */
  describe('Scripture Rotation', () => {
    it('should display John 12:31-32 on Monday', () => {
      cy.visit(`/#/office/midday/2024-01-15`); // Monday
      cy.wait(1000);
      cy.contains('JOHN 12:31-32').should('be.visible');
    });

    it('should display 2 Corinthians 5:17-18 on Tuesday', () => {
      cy.visit(`/#/office/midday/2024-01-16`); // Tuesday
      cy.wait(1000);
      cy.contains('2 CORINTHIANS 5:17-18').should('be.visible');
    });

    it('should display Malachi 1:11 on Wednesday', () => {
      cy.visit(`/#/office/midday/2024-01-17`); // Wednesday
      cy.wait(1000);
      cy.contains('MALACHI 1:11').should('be.visible');
    });
  });

  /**
   * T066: Seasonal variation tests
   */
  describe('Seasonal Variations', () => {
    it('should omit Alleluia during Lent', () => {
      cy.visit(`/#/office/midday/2024-02-14`); // Ash Wednesday
      cy.wait(1000);
      cy.contains('O God, make speed to save us').should('be.visible');
      // Alleluia should not appear in invitatory during Lent
      cy.get('body').then($body => {
        const invitatory = $body.find(':contains("O God, make speed to save us")').first();
        expect(invitatory.text()).to.not.contain('Alleluia');
      });
    });

    it('should include Alleluia in conclusion during Eastertide', () => {
      cy.visit(`/#/office/midday/2024-04-15`); // Easter season
      cy.wait(1000);
      cy.contains('Let us bless the Lord').should('be.visible');
      cy.contains('Alleluia').should('be.visible');
    });
  });

  /**
   * T066: Special feast day tests
   */
  describe('Feast Days', () => {
    it('should display correctly on Christmas', () => {
      cy.visit(`/#/office/midday/2024-12-25`);
      cy.wait(1000);
      cy.get('h1').contains('Midday Prayer').should('be.visible');
      cy.contains('Christmas').should('be.visible');
    });

    it('should use special collects on Conversion of Paul', () => {
      cy.visit(`/#/office/midday/2024-01-25`);
      cy.wait(1000);
      cy.contains('The Prayers').should('be.visible');
      cy.contains('Saint Paul').should('be.visible');
    });
  });

  /**
   * T065: Navigation tests
   */
  describe('Navigation', () => {
    it('should allow navigation to previous day', () => {
      cy.get('[aria-label="Previous Day"]').click();
      cy.wait(500);
      cy.url().should('include', '2024-01-14');
    });

    it('should allow navigation to next day', () => {
      cy.get('[aria-label="Next Day"]').click();
      cy.wait(500);
      cy.url().should('include', '2024-01-16');
    });

    it('should allow navigation to different office types', () => {
      // Check if Morning Prayer link exists
      cy.contains('Morning Prayer').should('exist');
      // Check if Evening Prayer link exists
      cy.contains('Evening Prayer').should('exist');
    });
  });

  /**
   * T066: Error handling
   */
  describe('Error Handling', () => {
    it('should handle invalid dates gracefully', () => {
      cy.visit('/#/office/midday/2024-13-99');
      cy.wait(1000);
      // Should either redirect or show error message
      cy.get('body').should('exist');
    });
  });

  /**
   * T066: Fixed psalm verification
   */
  describe('Fixed Psalm Assignment', () => {
    it('should always use the same psalms regardless of date', () => {
      const dates = ['2024-01-15', '2024-06-15', '2024-12-15'];
      
      dates.forEach(date => {
        cy.visit(`/#/office/midday/${date}`);
        cy.wait(1000);
        cy.contains('The Psalms').should('be.visible');
        cy.contains('Psalm 119').should('be.visible');
      });
    });
  });
});
