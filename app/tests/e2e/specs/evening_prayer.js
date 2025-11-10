/**
 * E2E tests for Evening Prayer (Daily Office)
 * 
 * Validates: FR-002 (Display Evening Prayer with all required liturgical components)
 * 
 * Tests verify that Evening Prayer displays correctly in the browser with all
 * liturgical elements visible and in the correct sequence, and that psalm assignments
 * differ from Morning Prayer.
 */

describe('Evening Prayer E2E Tests', () => {
  // Test viewing Evening Prayer for a specific date
  describe('T054: View Evening Prayer for today', () => {
    it('should load Evening Prayer page successfully', () => {
      // Get today's date
      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0');
      const day = String(today.getDate()).padStart(2, '0');

      // Intercept API call to backend
      cy.intercept('GET', `**/api/office/evening_prayer/${year}/${month}/${day}*`).as('getEveningPrayer');
      
      // Visit Evening Prayer page
      cy.visit(`/evening_prayer/${year}/${month}/${day}`);
      
      // Wait for API response
      cy.wait('@getEveningPrayer').then((interception) => {
        // Verify API returned successfully
        expect(interception.response.statusCode).to.equal(200);
        expect(interception.response.body).to.have.property('modules');
        
        // Log response for debugging
        cy.log('Evening Prayer API Response:', JSON.stringify(interception.response.body, null, 2));
      });

      // Verify page title
      cy.title().should('include', 'Evening Prayer');
    });

    it('should display calendar card with date information', () => {
      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0');
      const day = String(today.getDate()).padStart(2, '0');

      cy.visit(`/evening_prayer/${year}/${month}/${day}`);
      
      // Wait for page to load
      cy.get('.calendar-card', { timeout: 10000 }).should('be.visible');
      
      // Verify date is displayed
      cy.get('.calendar-card').should('contain.text', year);
    });
  });

  describe('T055: Evening Prayer displays all elements correctly', () => {
    beforeEach(() => {
      // Use a fixed date for consistent testing (Christmas Day)
      const year = 2024;
      const month = '12';
      const day = '25';

      cy.intercept('GET', `**/api/office/evening_prayer/${year}/${month}/${day}*`).as('getEveningPrayer');
      cy.visit(`/evening_prayer/${year}/${month}/${day}`);
      cy.wait('@getEveningPrayer', { timeout: 15000 });
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

    it('should display invitatory', () => {
      // Evening Prayer uses standard invitatory
      cy.get('body').should('satisfy', ($body) => {
        const text = $body.text();
        return text.includes('O God, make speed') || 
               text.includes('O Lord, make haste') ||
               text.includes('Invitatory');
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

    it('should display first canticle (Magnificat)', () => {
      // Evening Prayer typically uses Magnificat as first canticle
      cy.get('body').should('satisfy', ($body) => {
        const text = $body.text();
        return text.includes('Magnificat') || 
               text.includes('My soul magnifies the Lord') ||
               text.includes('Canticle');
      });
    });

    it('should display second reading', () => {
      // Verify second lesson is present
      cy.contains('The Second Lesson', { timeout: 10000 }).should('be.visible');
    });

    it('should display second canticle (Nunc Dimittis)', () => {
      // Evening Prayer typically uses Nunc Dimittis as second canticle
      cy.get('body').should('satisfy', ($body) => {
        const text = $body.text();
        return text.includes('Nunc Dimittis') || 
               text.includes('Lord, now let your servant depart in peace') ||
               text.includes('Canticle');
      });
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

    it('should display suffrages with saints', () => {
      // Evening Prayer suffrages include references to saints
      cy.get('body').should('satisfy', ($body) => {
        const text = $body.text();
        return text.includes('Blessed Virgin Mary') || 
               text.includes('Show us your mercy') ||
               text.includes('Suffrage');
      });
    });

    it('should display collects of the day', () => {
      // Verify collect of the day is present
      cy.get('body').should('contain.text', 'Collect');
    });

    it('should display evening collects', () => {
      // Verify evening-specific prayers/collects are present
      cy.get('body').should('satisfy', ($body) => {
        const text = $body.text();
        // Check for common evening collect phrases
        return text.includes('Lighten our darkness') || 
               text.includes('peace which the world cannot give') ||
               text.includes('Almighty');
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
        return text.includes('Morning Prayer') || 
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

  describe('T055: Verify psalm assignments differ from Morning Prayer', () => {
    it('should have different psalm assignments than Morning Prayer for same date', () => {
      // Use a regular day (not a feast) for clearer difference
      const year = 2024;
      const month = '06';
      const day = '15';

      // Get Evening Prayer data
      cy.intercept('GET', `**/api/office/evening_prayer/${year}/${month}/${day}*`).as('getEveningPrayer');
      cy.visit(`/evening_prayer/${year}/${month}/${day}`);
      cy.wait('@getEveningPrayer', { timeout: 15000 }).then((epInterception) => {
        const epModules = epInterception.response.body.modules;
        
        // Find psalms module in Evening Prayer
        const epPsalmsModule = epModules.find(module => 
          module.name && module.name.includes('Psalms')
        );
        
        // Now get Morning Prayer data for comparison
        cy.intercept('GET', `**/api/office/morning_prayer/${year}/${month}/${day}*`).as('getMorningPrayer');
        cy.visit(`/morning_prayer/${year}/${month}/${day}`);
        cy.wait('@getMorningPrayer', { timeout: 15000 }).then((mpInterception) => {
          const mpModules = mpInterception.response.body.modules;
          
          // Find psalms module in Morning Prayer
          const mpPsalmsModule = mpModules.find(module =>
            module.name && module.name.includes('Psalms')
          );
          
          // Verify both have psalms
          expect(epPsalmsModule).to.exist;
          expect(mpPsalmsModule).to.exist;
          
          // Verify psalms differ
          // The data structure may vary, but we can check the module data
          const epData = JSON.stringify(epPsalmsModule);
          const mpData = JSON.stringify(mpPsalmsModule);
          
          expect(epData).to.not.equal(mpData, 'Evening Prayer and Morning Prayer should have different psalm assignments');
        });
      });
    });

    it('should display different psalm numbers in UI for Evening vs Morning Prayer', () => {
      // Use a regular day
      const year = 2024;
      const month = '06';
      const day = '15';

      // Visit Evening Prayer and extract psalm citations
      cy.visit(`/evening_prayer/${year}/${month}/${day}`);
      cy.wait(2000); // Wait for page to fully load
      
      // Get the psalms text from Evening Prayer
      cy.get('body').then(($epBody) => {
        const epText = $epBody.text();
        
        // Extract psalm numbers (look for "Psalm" followed by numbers)
        const epPsalmMatch = epText.match(/The Psalms? Appointed[\s\S]{0,200}Psalm\s+(\d+)/);
        const epPsalmNumber = epPsalmMatch ? epPsalmMatch[1] : null;
        
        // Now visit Morning Prayer
        cy.visit(`/morning_prayer/${year}/${month}/${day}`);
        cy.wait(2000);
        
        cy.get('body').then(($mpBody) => {
          const mpText = $mpBody.text();
          
          // Extract psalm numbers from Morning Prayer
          const mpPsalmMatch = mpText.match(/The Psalms? Appointed[\s\S]{0,200}Psalm\s+(\d+)/);
          const mpPsalmNumber = mpPsalmMatch ? mpPsalmMatch[1] : null;
          
          // Verify we found psalms in both
          expect(epPsalmNumber).to.not.be.null;
          expect(mpPsalmNumber).to.not.be.null;
          
          // Verify they're different
          expect(epPsalmNumber).to.not.equal(mpPsalmNumber, 
            `Evening Prayer Psalm ${epPsalmNumber} should differ from Morning Prayer Psalm ${mpPsalmNumber}`);
        });
      });
    });
  });

  describe('Additional Evening Prayer Tests', () => {
    it('should handle API errors gracefully', () => {
      // Test with an invalid date
      const year = 2024;
      const month = '13'; // Invalid month
      const day = '32'; // Invalid day

      cy.intercept('GET', `**/api/office/evening_prayer/${year}/${month}/${day}*`, {
        statusCode: 404,
        body: { error: 'Not found' }
      }).as('getInvalidEveningPrayer');
      
      cy.visit(`/evening_prayer/${year}/${month}/${day}`, { failOnStatusCode: false });
      
      // Should show error message or redirect
      cy.get('body').should('satisfy', ($body) => {
        const text = $body.text();
        return text.includes('error') || 
               text.includes('not found') ||
               text.includes('Not Found');
      });
    });

    it('should load Evening Prayer for a feast day (Easter)', () => {
      // Test Easter Sunday 2024
      const year = 2024;
      const month = '03';
      const day = '31';

      cy.intercept('GET', `**/api/office/evening_prayer/${year}/${month}/${day}*`).as('getEasterEP');
      cy.visit(`/evening_prayer/${year}/${month}/${day}`);
      cy.wait('@getEasterEP', { timeout: 15000 });

      // Verify Easter elements appear
      cy.get('body', { timeout: 10000 }).should('satisfy', ($body) => {
        const text = $body.text();
        return text.includes('Alleluia') || text.includes('Easter');
      });
    });

    it('should load Evening Prayer for Advent (O Antiphons)', () => {
      // Test December 17 (first O Antiphon day)
      const year = 2024;
      const month = '12';
      const day = '17';

      cy.intercept('GET', `**/api/office/evening_prayer/${year}/${month}/${day}*`).as('getAdventEP');
      cy.visit(`/evening_prayer/${year}/${month}/${day}`);
      cy.wait('@getAdventEP', { timeout: 15000 });

      // Verify O Antiphon appears (Dec 17-23)
      cy.get('body', { timeout: 10000 }).should('satisfy', ($body) => {
        const text = $body.text();
        // O Antiphons include Latin text and "O come" refrain
        return text.includes('O Sapientia') || 
               text.includes('O Wisdom') ||
               text.includes('O come');
      });
    });

    it('should load Evening Prayer for a regular feria day', () => {
      // Test a regular weekday (June 15, 2024 - Saturday)
      const year = 2024;
      const month = '06';
      const day = '15';

      cy.intercept('GET', `**/api/office/evening_prayer/${year}/${month}/${day}*`).as('getFeriaEP');
      cy.visit(`/evening_prayer/${year}/${month}/${day}`);
      cy.wait('@getFeriaEP', { timeout: 15000 });

      // Verify page loads and has basic elements
      cy.contains(/The Psalms? Appointed/i, { timeout: 10000 }).should('be.visible');
      cy.contains('The First Lesson', { timeout: 10000 }).should('be.visible');
    });
  });
});
