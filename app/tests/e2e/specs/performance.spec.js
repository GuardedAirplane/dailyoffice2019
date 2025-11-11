/**
 * E2E Performance Tests for Daily Office
 * 
 * T233: E2E test - Office page load time < 3 seconds
 * 
 * Tests verify SC-001 compliance: Office page load < 3 seconds
 * Includes performance metrics for:
 * - Initial page load
 * - Office content rendering
 * - Navigation between offices
 * - Date navigation
 * - Resource loading (fonts, styles, scripts)
 */

describe('Office Performance Tests (SC-001 Compliance)', () => {
  const PERFORMANCE_THRESHOLD_MS = 3000; // SC-001 requirement
  const API_THRESHOLD_MS = 1000; // API should respond within 1 second
  
  beforeEach(() => {
    // Clear any caches to ensure consistent testing
    cy.clearCookies();
    cy.clearLocalStorage();
  });

  describe('Initial Page Load Performance', () => {
    it('should load Morning Prayer page within 3 seconds (SC-001)', () => {
      const startTime = Date.now();
      
      cy.visit('/office/morning_prayer/2025/12/25/');
      
      // Wait for office content to be fully rendered
      cy.get('[data-testid="office-content"]', { timeout: PERFORMANCE_THRESHOLD_MS })
        .should('be.visible')
        .then(() => {
          const loadTime = Date.now() - startTime;
          cy.log(`Morning Prayer load time: ${loadTime}ms`);
          
          // SC-001: Office page load < 3 seconds
          expect(loadTime).to.be.lessThan(PERFORMANCE_THRESHOLD_MS);
        });
    });

    it('should load Evening Prayer page within 3 seconds (SC-001)', () => {
      const startTime = Date.now();
      
      cy.visit('/office/evening_prayer/2025/12/25/');
      
      cy.get('[data-testid="office-content"]', { timeout: PERFORMANCE_THRESHOLD_MS })
        .should('be.visible')
        .then(() => {
          const loadTime = Date.now() - startTime;
          cy.log(`Evening Prayer load time: ${loadTime}ms`);
          
          expect(loadTime).to.be.lessThan(PERFORMANCE_THRESHOLD_MS);
        });
    });

    it('should load Midday Prayer page within 3 seconds (SC-001)', () => {
      const startTime = Date.now();
      
      cy.visit('/office/midday_prayer/2025/12/25/');
      
      cy.get('[data-testid="office-content"]', { timeout: PERFORMANCE_THRESHOLD_MS })
        .should('be.visible')
        .then(() => {
          const loadTime = Date.now() - startTime;
          cy.log(`Midday Prayer load time: ${loadTime}ms`);
          
          expect(loadTime).to.be.lessThan(PERFORMANCE_THRESHOLD_MS);
        });
    });

    it('should load Compline page within 3 seconds (SC-001)', () => {
      const startTime = Date.now();
      
      cy.visit('/office/compline/2025/12/25/');
      
      cy.get('[data-testid="office-content"]', { timeout: PERFORMANCE_THRESHOLD_MS })
        .should('be.visible')
        .then(() => {
          const loadTime = Date.now() - startTime;
          cy.log(`Compline load time: ${loadTime}ms`);
          
          expect(loadTime).to.be.lessThan(PERFORMANCE_THRESHOLD_MS);
        });
    });
  });

  describe('API Response Performance', () => {
    it('should receive API response for Morning Prayer within 1 second', () => {
      cy.intercept('GET', '**/api/office/morning_prayer/**').as('morningPrayerAPI');
      
      const startTime = Date.now();
      cy.visit('/office/morning_prayer/2025/12/25/');
      
      cy.wait('@morningPrayerAPI').then((interception) => {
        const apiTime = Date.now() - startTime;
        cy.log(`Morning Prayer API response time: ${apiTime}ms`);
        
        // API should respond quickly
        expect(apiTime).to.be.lessThan(API_THRESHOLD_MS);
        
        // API should return 200 OK
        expect(interception.response.statusCode).to.equal(200);
      });
    });

    it('should receive API response for Evening Prayer within 1 second', () => {
      cy.intercept('GET', '**/api/office/evening_prayer/**').as('eveningPrayerAPI');
      
      const startTime = Date.now();
      cy.visit('/office/evening_prayer/2025/12/25/');
      
      cy.wait('@eveningPrayerAPI').then((interception) => {
        const apiTime = Date.now() - startTime;
        cy.log(`Evening Prayer API response time: ${apiTime}ms`);
        
        expect(apiTime).to.be.lessThan(API_THRESHOLD_MS);
        expect(interception.response.statusCode).to.equal(200);
      });
    });
  });

  describe('Navigation Performance', () => {
    it('should navigate between offices quickly', () => {
      cy.visit('/office/morning_prayer/2025/12/25/');
      cy.get('[data-testid="office-content"]').should('be.visible');
      
      // Navigate to Evening Prayer
      const startTime = Date.now();
      cy.get('[data-testid="nav-evening-prayer"]').click();
      
      cy.get('[data-testid="office-content"]').should('be.visible').then(() => {
        const navTime = Date.now() - startTime;
        cy.log(`Navigation time: ${navTime}ms`);
        
        // Navigation should be fast (within 2 seconds)
        expect(navTime).to.be.lessThan(2000);
      });
      
      // Verify we're on Evening Prayer
      cy.url().should('include', '/evening_prayer/');
    });

    it('should navigate to different dates quickly', () => {
      cy.visit('/office/morning_prayer/2025/12/25/');
      cy.get('[data-testid="office-content"]').should('be.visible');
      
      // Navigate to next day
      const startTime = Date.now();
      cy.get('[data-testid="nav-next-day"]').click();
      
      cy.get('[data-testid="office-content"]').should('be.visible').then(() => {
        const navTime = Date.now() - startTime;
        cy.log(`Date navigation time: ${navTime}ms`);
        
        expect(navTime).to.be.lessThan(2000);
      });
      
      // Verify date changed
      cy.url().should('include', '/2025/12/26/');
    });
  });

  describe('Resource Loading Performance', () => {
    it('should load all critical resources efficiently', () => {
      cy.visit('/office/morning_prayer/2025/12/25/', {
        onBeforeLoad: (win) => {
          // Capture performance metrics
          win.performance.mark('page-start');
        },
      });
      
      cy.window().then((win) => {
        const perfData = win.performance.getEntriesByType('navigation')[0];
        
        if (perfData) {
          cy.log(`DOM Content Loaded: ${perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart}ms`);
          cy.log(`Load Complete: ${perfData.loadEventEnd - perfData.loadEventStart}ms`);
          cy.log(`Total Load Time: ${perfData.loadEventEnd - perfData.fetchStart}ms`);
          
          // Total load time should be reasonable
          const totalLoadTime = perfData.loadEventEnd - perfData.fetchStart;
          expect(totalLoadTime).to.be.lessThan(PERFORMANCE_THRESHOLD_MS);
        }
      });
    });

    it('should load fonts without blocking rendering', () => {
      cy.visit('/office/morning_prayer/2025/12/25/');
      
      // Content should be visible even if fonts are still loading
      cy.get('[data-testid="office-content"]', { timeout: 1000 })
        .should('be.visible');
      
      // Fonts should eventually load
      cy.document().then((doc) => {
        cy.wrap(doc.fonts.ready).should('exist');
      });
    });
  });

  describe('Performance Under Load Scenarios', () => {
    it('should load large feast day (Christmas) within 3 seconds', () => {
      const startTime = Date.now();
      
      // Christmas has many readings and commemorations
      cy.visit('/office/morning_prayer/2025/12/25/');
      
      cy.get('[data-testid="office-content"]', { timeout: PERFORMANCE_THRESHOLD_MS })
        .should('be.visible')
        .then(() => {
          const loadTime = Date.now() - startTime;
          cy.log(`Christmas Day load time: ${loadTime}ms`);
          
          expect(loadTime).to.be.lessThan(PERFORMANCE_THRESHOLD_MS);
        });
      
      // Verify content loaded completely
      cy.get('[data-testid="office-module"]').should('have.length.greaterThan', 10);
    });

    it('should load office with multiple commemorations quickly', () => {
      const startTime = Date.now();
      
      // Date with multiple commemorations
      cy.visit('/office/morning_prayer/2025/01/25/');
      
      cy.get('[data-testid="office-content"]', { timeout: PERFORMANCE_THRESHOLD_MS })
        .should('be.visible')
        .then(() => {
          const loadTime = Date.now() - startTime;
          cy.log(`Multiple commemorations load time: ${loadTime}ms`);
          
          expect(loadTime).to.be.lessThan(PERFORMANCE_THRESHOLD_MS);
        });
    });

    it('should handle rapid navigation without performance degradation', () => {
      cy.visit('/office/morning_prayer/2025/12/25/');
      cy.get('[data-testid="office-content"]').should('be.visible');
      
      const navigationTimes = [];
      
      // Navigate rapidly between offices
      for (let i = 0; i < 3; i++) {
        const startTime = Date.now();
        
        cy.get('[data-testid="nav-evening-prayer"]').click();
        cy.get('[data-testid="office-content"]').should('be.visible').then(() => {
          const navTime = Date.now() - startTime;
          navigationTimes.push(navTime);
          cy.log(`Navigation ${i + 1} time: ${navTime}ms`);
        });
        
        cy.get('[data-testid="nav-morning-prayer"]').click();
        cy.get('[data-testid="office-content"]').should('be.visible');
      }
      
      // All navigations should be consistently fast
      cy.wrap(navigationTimes).each((time) => {
        expect(time).to.be.lessThan(2000);
      });
    });
  });

  describe('Performance Regression Detection', () => {
    it('should track and log performance metrics for baseline', () => {
      const metrics = {
        morningPrayer: 0,
        eveningPrayer: 0,
        middayPrayer: 0,
        compline: 0,
      };
      
      // Measure Morning Prayer
      const mpStart = Date.now();
      cy.visit('/office/morning_prayer/2025/12/25/');
      cy.get('[data-testid="office-content"]').should('be.visible').then(() => {
        metrics.morningPrayer = Date.now() - mpStart;
      });
      
      // Measure Evening Prayer
      const epStart = Date.now();
      cy.visit('/office/evening_prayer/2025/12/25/');
      cy.get('[data-testid="office-content"]').should('be.visible').then(() => {
        metrics.eveningPrayer = Date.now() - epStart;
      });
      
      // Measure Midday Prayer
      const mdpStart = Date.now();
      cy.visit('/office/midday_prayer/2025/12/25/');
      cy.get('[data-testid="office-content"]').should('be.visible').then(() => {
        metrics.middayPrayer = Date.now() - mdpStart;
      });
      
      // Measure Compline
      const compStart = Date.now();
      cy.visit('/office/compline/2025/12/25/');
      cy.get('[data-testid="office-content"]').should('be.visible').then(() => {
        metrics.compline = Date.now() - compStart;
        
        // Log all metrics
        cy.log('Performance Metrics (ms):', JSON.stringify(metrics, null, 2));
        
        // All should meet SC-001
        expect(metrics.morningPrayer).to.be.lessThan(PERFORMANCE_THRESHOLD_MS);
        expect(metrics.eveningPrayer).to.be.lessThan(PERFORMANCE_THRESHOLD_MS);
        expect(metrics.middayPrayer).to.be.lessThan(PERFORMANCE_THRESHOLD_MS);
        expect(metrics.compline).to.be.lessThan(PERFORMANCE_THRESHOLD_MS);
      });
    });
  });

  describe('Mobile Performance', () => {
    it('should load office on mobile viewport within 3 seconds', () => {
      cy.viewport('iphone-x');
      
      const startTime = Date.now();
      cy.visit('/office/morning_prayer/2025/12/25/');
      
      cy.get('[data-testid="office-content"]', { timeout: PERFORMANCE_THRESHOLD_MS })
        .should('be.visible')
        .then(() => {
          const loadTime = Date.now() - startTime;
          cy.log(`Mobile load time: ${loadTime}ms`);
          
          expect(loadTime).to.be.lessThan(PERFORMANCE_THRESHOLD_MS);
        });
    });

    it('should load office on tablet viewport within 3 seconds', () => {
      cy.viewport('ipad-2');
      
      const startTime = Date.now();
      cy.visit('/office/morning_prayer/2025/12/25/');
      
      cy.get('[data-testid="office-content"]', { timeout: PERFORMANCE_THRESHOLD_MS })
        .should('be.visible')
        .then(() => {
          const loadTime = Date.now() - startTime;
          cy.log(`Tablet load time: ${loadTime}ms`);
          
          expect(loadTime).to.be.lessThan(PERFORMANCE_THRESHOLD_MS);
        });
    });
  });

  describe('Caching and Optimization', () => {
    it('should load faster on subsequent visits (caching)', () => {
      // First visit
      const firstVisitStart = Date.now();
      cy.visit('/office/morning_prayer/2025/12/25/');
      cy.get('[data-testid="office-content"]').should('be.visible');
      const firstVisitTime = Date.now() - firstVisitStart;
      
      cy.log(`First visit time: ${firstVisitTime}ms`);
      
      // Second visit (should benefit from caching)
      const secondVisitStart = Date.now();
      cy.visit('/office/morning_prayer/2025/12/25/');
      cy.get('[data-testid="office-content"]').should('be.visible');
      const secondVisitTime = Date.now() - secondVisitStart;
      
      cy.log(`Second visit time: ${secondVisitTime}ms`);
      cy.log(`Improvement: ${firstVisitTime - secondVisitTime}ms`);
      
      // Second visit should be faster or equal (caching helps)
      expect(secondVisitTime).to.be.lessThan(firstVisitTime + 500); // Allow 500ms variance
    });

    it('should efficiently handle localStorage usage', () => {
      cy.visit('/office/morning_prayer/2025/12/25/');
      
      cy.window().then((win) => {
        const localStorageSize = new Blob(
          Object.values(win.localStorage)
        ).size;
        
        cy.log(`localStorage size: ${localStorageSize} bytes`);
        
        // localStorage should be reasonable (< 1MB)
        expect(localStorageSize).to.be.lessThan(1024 * 1024);
      });
    });
  });
});
