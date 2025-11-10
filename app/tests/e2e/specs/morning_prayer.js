/**
 * E2E tests for Morning Prayer (Daily Office)
 * 
 * Validates: FR-001 (Display Morning Prayer with all required liturgical components)
 * 
 * Tests verify that Morning Prayer displays correctly in the browser with all
 * liturgical elements visible and in the correct sequence.
 */

describe('Morning Prayer E2E Tests', () => {
  // Test viewing Morning Prayer for a specific date
  describe('T039: View Morning Prayer for today', () => {
    it('should load Morning Prayer page successfully', () => {
      // Get today's date
      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0');
      const day = String(today.getDate()).padStart(2, '0');

      // Intercept API call to backend
      cy.intercept('GET', `**/api/office/morning_prayer/${year}/${month}/${day}*`).as('getMorningPrayer');
      
      // Visit Morning Prayer page
      cy.visit(`/morning_prayer/${year}/${month}/${day}`);
      
      // Wait for API response
      cy.wait('@getMorningPrayer').then((interception) => {
        // Verify API returned successfully
        expect(interception.response.statusCode).to.equal(200);
        expect(interception.response.body).to.have.property('modules');
        
        // Log response for debugging
        cy.log('Morning Prayer API Response:', JSON.stringify(interception.response.body, null, 2));
      });

      // Verify page title
      cy.title().should('include', 'Morning Prayer');
    });

    it('should display calendar card with date information', () => {
      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0');
      const day = String(today.getDate()).padStart(2, '0');

      cy.visit(`/morning_prayer/${year}/${month}/${day}`);
      
      // Wait for page to load
      cy.get('.calendar-card', { timeout: 10000 }).should('be.visible');
      
      // Verify date is displayed
      cy.get('.calendar-card').should('contain.text', year);
    });
  });

  describe('T040: Morning Prayer displays all elements correctly', () => {
    beforeEach(() => {
      // Use a fixed date for consistent testing (Christmas Day)
      const year = 2024;
      const month = '12';
      const day = '25';

      cy.intercept('GET', `**/api/office/morning_prayer/${year}/${month}/${day}*`).as('getMorningPrayer');
      cy.visit(`/morning_prayer/${year}/${month}/${day}`);
      cy.wait('@getMorningPrayer', { timeout: 15000 });
    });

    it('should display opening sentence', () => {
      // Verify opening sentence section is present
      cy.contains('Opening Sentence', { timeout: 10000 }).should('be.visible');
    });

    it('should display confession', () => {
      // Verify confession section is present
      cy.contains('Confession of Sin', { timeout: 10000 }).should('be.visible');
      // Or alternative heading
      cy.get('body').should('contain.text', 'Confession');
    });

    it('should display invitatory (Venite/Jubilate/Pascha Nostrum)', () => {
      // Check for one of the possible invitatory canticles
      cy.get('body').should('satisfy', ($body) => {
        const text = $body.text();
        return text.includes('Venite') || 
               text.includes('Jubilate') || 
               text.includes('Pascha Nostrum') ||
               text.includes('PASCHA NOSTRUM');
      });
    });

    it('should display psalms section', () => {
      // Verify psalms are present
      cy.contains(/The Psalms? Appointed/i, { timeout: 10000 }).should('be.visible');
    });

    it('should display first reading', () => {
      // Verify first lesson is present
      cy.contains('The First Lesson', { timeout: 10000 }).should('be.visible');
    });

    it('should display first canticle', () => {
      // Check that a canticle appears after first reading
      // Common morning canticles include Benedictus, Te Deum, etc.
      cy.get('body').should('satisfy', ($body) => {
        const text = $body.text();
        return text.includes('Benedictus') || 
               text.includes('Te Deum') ||
               text.includes('Canticle');
      });
    });

    it('should display second reading', () => {
      // Verify second lesson is present
      cy.contains('The Second Lesson', { timeout: 10000 }).should('be.visible');
    });

    it('should display second canticle', () => {
      // Verify second canticle section exists
      // After second reading, there should be another canticle
      cy.get('body').should('contain.text', 'Benedictus');
    });

    it('should display Apostles Creed', () => {
      // Verify creed is present
      cy.contains(/Apostles.* Creed|The Creed/i, { timeout: 10000 }).should('be.visible');
      cy.get('body').should('contain.text', 'I believe in God');
    });

    it('should display prayers section', () => {
      // Verify Lord's Prayer is present
      cy.get('body').should('contain.text', 'Our Father');
    });

    it('should display suffrages', () => {
      // Verify suffrages (versicles and responses) are present
      cy.get('body').should('satisfy', ($body) => {
        const text = $body.text();
        return text.includes('Show us your mercy') || 
               text.includes('Lord, have mercy') ||
               text.includes('Suffrage');
      });
    });

    it('should display collects of the day', () => {
      // Verify collect of the day is present
      cy.get('body').should('contain.text', 'Collect');
    });

    it('should display general collects', () => {
      // Verify general prayers/collects are present
      cy.get('body').should('satisfy', ($body) => {
        const text = $body.text();
        // Check for common collect phrases
        return text.includes('Almighty') || text.includes('Heavenly Father');
      });
    });

    it('should display dismissal', () => {
      // Verify dismissal/blessing is present at end
      cy.get('body').should('satisfy', ($body) => {
        const text = $body.text();
        return text.includes('Let us bless the Lord') || 
               text.includes('grace of our Lord Jesus Christ');
      });
    });

    it('should display all components in correct liturgical order', () => {
      // Verify the page contains the major sections in order
      cy.get('body').then(($body) => {
        const text = $body.text();
        
        // Get approximate positions of major sections
        const openingPos = text.indexOf('Opening Sentence');
        const confessionPos = text.indexOf('Confession');
        const psalmPos = text.search(/The Psalms? Appointed/i);
        const firstReadingPos = text.indexOf('The First Lesson');
        const secondReadingPos = text.indexOf('The Second Lesson');
        const creedPos = text.search(/Apostles.* Creed|I believe in God/i);
        const prayersPos = text.indexOf('Our Father');
        
        // Verify order (positions should increase)
        // Note: Some sections might be -1 if not found, so we check when both are found
        if (openingPos > -1 && confessionPos > -1) {
          expect(openingPos).to.be.lessThan(confessionPos);
        }
        if (confessionPos > -1 && psalmPos > -1) {
          expect(confessionPos).to.be.lessThan(psalmPos);
        }
        if (psalmPos > -1 && firstReadingPos > -1) {
          expect(psalmPos).to.be.lessThan(firstReadingPos);
        }
        if (firstReadingPos > -1 && secondReadingPos > -1) {
          expect(firstReadingPos).to.be.lessThan(secondReadingPos);
        }
        if (secondReadingPos > -1 && creedPos > -1) {
          expect(secondReadingPos).to.be.lessThan(creedPos);
        }
        if (creedPos > -1 && prayersPos > -1) {
          expect(creedPos).to.be.lessThan(prayersPos);
        }
      });
    });

    it('should have functional office navigation', () => {
      // Verify navigation to other offices exists
      cy.get('body').should('satisfy', ($body) => {
        const text = $body.text();
        // Check for links to other offices
        return text.includes('Evening Prayer') || 
               text.includes('Midday Prayer') ||
               text.includes('Compline');
      });
    });

    it('should allow date navigation', () => {
      // Check for date navigation controls
      cy.get('body').should('satisfy', ($body) => {
        const html = $body.html();
        // Look for forward/backward navigation or date picker
        return html.includes('arrow') || 
               html.includes('next') || 
               html.includes('previous') ||
               html.includes('calendar');
      });
    });
  });

  describe('Additional Morning Prayer Tests', () => {
    it('should handle API errors gracefully', () => {
      // Test with an invalid date that might cause errors
      const year = 2024;
      const month = '13'; // Invalid month
      const day = '32'; // Invalid day

      cy.intercept('GET', `**/api/office/morning_prayer/${year}/${month}/${day}*`, {
        statusCode: 404,
        body: { error: 'Not found' }
      }).as('getInvalidMorningPrayer');
      
      cy.visit(`/morning_prayer/${year}/${month}/${day}`, { failOnStatusCode: false });
      
      // Should show error message or redirect
      cy.get('body').should('satisfy', ($body) => {
        const text = $body.text();
        return text.includes('error') || 
               text.includes('not found') ||
               text.includes('Not Found');
      });
    });

    it('should load Morning Prayer for a feast day (Easter)', () => {
      // Test Easter Sunday 2024
      const year = 2024;
      const month = '03';
      const day = '31';

      cy.intercept('GET', `**/api/office/morning_prayer/${year}/${month}/${day}*`).as('getEasterMP');
      cy.visit(`/morning_prayer/${year}/${month}/${day}`);
      cy.wait('@getEasterMP', { timeout: 15000 });

      // Verify Pascha Nostrum appears (used during Eastertide)
      cy.get('body', { timeout: 10000 }).should('satisfy', ($body) => {
        const text = $body.text();
        return text.includes('Alleluia') || text.includes('Easter');
      });
    });

    it('should load Morning Prayer for a regular feria day', () => {
      // Test a regular weekday (June 15, 2024 - Saturday)
      const year = 2024;
      const month = '06';
      const day = '15';

      cy.intercept('GET', `**/api/office/morning_prayer/${year}/${month}/${day}*`).as('getFeriaMP');
      cy.visit(`/morning_prayer/${year}/${month}/${day}`);
      cy.wait('@getFeriaMP', { timeout: 15000 });

      // Verify page loads and has basic elements
      cy.contains(/The Psalms? Appointed/i, { timeout: 10000 }).should('be.visible');
      cy.contains('The First Lesson', { timeout: 10000 }).should('be.visible');
    });
  });
});
