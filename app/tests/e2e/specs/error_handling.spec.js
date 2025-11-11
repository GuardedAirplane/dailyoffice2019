/**
 * E2E tests for error handling and offline scenarios
 * 
 * Tests validate that the application handles API failures, network issues,
 * and offline scenarios gracefully with proper user feedback.
 * 
 * Test Coverage:
 * - T193: Bible Gateway API unavailability (mock)
 * - T194: Offline mode displays error indicator
 * - T195: Retry button functionality
 * 
 * FR Requirements:
 * - FR-022a: Display error with offline indicator
 * - FR-022b: Provide retry option
 * - FR-022c: Allow viewing cached content
 */

describe('Error Handling and Offline Scenarios', () => {
  beforeEach(() => {
    // Visit the office page before each test
    cy.visit('/office/morning_prayer/2025/12/25/')
  })

  describe('T193: API Unavailability Handling', () => {
    it('should display error message when Bible Gateway API is unavailable', () => {
      // FR-022a: Display error with offline indicator
      
      // Mock API failure by intercepting network requests
      cy.intercept('GET', '**/api/scripture/**', {
        statusCode: 503,
        body: { error: 'Service unavailable' }
      }).as('scriptureRequest')

      // Navigate to an office that would trigger scripture loading
      cy.visit('/office/morning_prayer/2025/1/1/')
      
      // Wait for API call to fail
      cy.wait('@scriptureRequest')

      // Should display error indicator (implementation dependent)
      // This test documents expected behavior - actual implementation may vary
      cy.get('[data-testid="error-message"]', { timeout: 5000 })
        .should('be.visible')
        .and('contain', 'unable to load')
    })

    it('should handle timeout errors gracefully', () => {
      // FR-022a: Timeout errors should be detected and displayed
      
      // Mock request timeout
      cy.intercept('GET', '**/api/scripture/**', {
        forceNetworkError: true
      }).as('timeoutRequest')

      cy.visit('/office/evening_prayer/2025/3/15/')
      
      // Should show network error message
      cy.wait('@timeoutRequest')
      cy.get('[data-testid="error-message"]', { timeout: 5000 })
        .should('be.visible')
    })

    it('should handle 500 server errors with user-friendly message', () => {
      // FR-022a: Server errors should show friendly error message
      
      cy.intercept('GET', '**/api/scripture/**', {
        statusCode: 500,
        body: { error: 'Internal server error' }
      }).as('serverError')

      cy.visit('/office/midday_prayer/2025/6/20/')
      
      cy.wait('@serverError')
      cy.get('[data-testid="error-message"]')
        .should('be.visible')
        .and('not.contain', '500') // Should show friendly message, not raw error
    })
  })

  describe('T194: Offline Mode Indicator', () => {
    it('should display offline indicator when network is unavailable', () => {
      // FR-022a: Display error with offline indicator
      
      // Simulate offline mode
      cy.intercept('GET', '**/api/**', { forceNetworkError: true })

      cy.visit('/office/compline/2025/8/10/')

      // Should show offline indicator
      cy.get('[data-testid="offline-indicator"]', { timeout: 5000 })
        .should('be.visible')
        .and('contain', 'offline')
    })

    it('should indicate partial functionality when API unavailable', () => {
      // FR-022c: Allow viewing cached content
      
      // Mock API failure
      cy.intercept('GET', '**/api/scripture/**', {
        statusCode: 503
      }).as('apiFailure')

      cy.visit('/office/morning_prayer/2025/5/1/')
      
      cy.wait('@apiFailure')

      // Office structure should still load (from cache or fallback)
      cy.get('[data-testid="office-content"]')
        .should('exist')

      // But should show warning about missing scripture
      cy.get('[data-testid="warning-message"]')
        .should('be.visible')
        .and('contain', 'scripture')
    })

    it('should update indicator when connection is restored', () => {
      // FR-022a: Offline indicator should update when back online
      
      // Start offline
      cy.intercept('GET', '**/api/**', { forceNetworkError: true }).as('offline')
      
      cy.visit('/office/evening_prayer/2025/7/4/')
      cy.wait('@offline')

      // Verify offline indicator appears
      cy.get('[data-testid="offline-indicator"]')
        .should('be.visible')

      // Simulate connection restored (would need actual implementation)
      // This test documents expected behavior
      
      // Re-enable network
      cy.intercept('GET', '**/api/**').as('online')
      
      // Trigger retry or navigation
      cy.get('[data-testid="retry-button"]').click()
      
      cy.wait('@online')

      // Offline indicator should disappear
      cy.get('[data-testid="offline-indicator"]')
        .should('not.exist')
    })
  })

  describe('T195: Retry Button Functionality', () => {
    it('should provide retry button when API fails', () => {
      // FR-022b: Provide retry option
      
      cy.intercept('GET', '**/api/scripture/**', {
        statusCode: 503
      }).as('failedRequest')

      cy.visit('/office/morning_prayer/2025/2/14/')
      
      cy.wait('@failedRequest')

      // Retry button should be visible
      cy.get('[data-testid="retry-button"]')
        .should('be.visible')
        .and('contain', 'retry')
    })

    it('should retry failed request when retry button clicked', () => {
      // FR-022b: Retry button should trigger new API call
      
      let requestCount = 0

      cy.intercept('GET', '**/api/scripture/**', (req) => {
        requestCount++
        if (requestCount === 1) {
          // First request fails
          req.reply({ statusCode: 503 })
        } else {
          // Second request succeeds
          req.reply({ statusCode: 200, body: { text: 'Scripture text' } })
        }
      }).as('retryableRequest')

      cy.visit('/office/evening_prayer/2025/4/15/')
      
      // Wait for first failure
      cy.wait('@retryableRequest')

      // Click retry
      cy.get('[data-testid="retry-button"]').click()

      // Wait for retry attempt
      cy.wait('@retryableRequest')

      // Error should be gone, content should load
      cy.get('[data-testid="error-message"]')
        .should('not.exist')
      
      cy.get('[data-testid="scripture-content"]')
        .should('be.visible')
    })

    it('should retry all failed components', () => {
      // FR-022b: Retry should attempt to reload all failed content
      
      cy.intercept('GET', '**/api/**', {
        statusCode: 503
      }).as('allFailed')

      cy.visit('/office/midday_prayer/2025/9/20/')
      
      cy.wait('@allFailed')

      // Global retry button should exist
      cy.get('[data-testid="retry-all-button"]')
        .should('be.visible')

      // Clicking retry should reload page or refetch data
      cy.intercept('GET', '**/api/**', { statusCode: 200 }).as('retrySuccess')
      
      cy.get('[data-testid="retry-all-button"]').click()
      
      cy.wait('@retrySuccess')

      // Content should load successfully
      cy.get('[data-testid="office-content"]')
        .should('be.visible')
    })

    it('should show retry limit after multiple failures', () => {
      // FR-022b: Should prevent infinite retry loops
      
      cy.intercept('GET', '**/api/**', {
        statusCode: 503
      }).as('persistentFailure')

      cy.visit('/office/compline/2025/11/1/')
      
      cy.wait('@persistentFailure')

      // Try retrying multiple times
      for (let i = 0; i < 3; i++) {
        cy.get('[data-testid="retry-button"]').click()
        cy.wait('@persistentFailure')
      }

      // After multiple failures, should show different message
      cy.get('[data-testid="error-message"]')
        .should('contain', 'persist')
        .or('contain', 'offline')
    })
  })

  describe('Cached Content Fallback', () => {
    it('should display cached scripture when API fails', () => {
      // FR-022c: Allow viewing cached content
      
      // Assume some content is cached from previous visit
      // First visit succeeds and caches data
      cy.intercept('GET', '**/api/scripture/**', {
        statusCode: 200,
        body: { text: 'Cached scripture text' }
      }).as('cacheSetup')

      cy.visit('/office/morning_prayer/2025/12/25/')
      cy.wait('@cacheSetup')

      // Second visit fails API but uses cache
      cy.intercept('GET', '**/api/scripture/**', {
        statusCode: 503
      }).as('apiFailure')

      cy.reload()
      cy.wait('@apiFailure')

      // Cached content should still display
      cy.get('[data-testid="scripture-content"]')
        .should('be.visible')
        .and('contain', 'scripture')

      // But should indicate it's cached/offline
      cy.get('[data-testid="cache-indicator"]')
        .should('be.visible')
    })

    it('should gracefully degrade when no cache available', () => {
      // FR-022c: When cache unavailable, show placeholder
      
      cy.intercept('GET', '**/api/scripture/**', {
        statusCode: 503
      }).as('noCache')

      cy.visit('/office/evening_prayer/2025/1/10/')
      cy.wait('@noCache')

      // Should show placeholder or message
      cy.get('[data-testid="scripture-placeholder"]')
        .should('be.visible')
        .and('contain', 'unavailable')
    })
  })

  describe('Progressive Loading and Error Recovery', () => {
    it('should load office structure even if scriptures fail', () => {
      // FR-022c: Core office should load even with partial failures
      
      // Mock scripture failures but allow other content
      cy.intercept('GET', '**/api/scripture/**', {
        statusCode: 503
      })
      cy.intercept('GET', '**/api/office/**', {
        statusCode: 200,
        body: { /* mock office data */ }
      })

      cy.visit('/office/morning_prayer/2025/6/15/')

      // Office structure should be visible
      cy.get('[data-testid="office-heading"]').should('be.visible')
      cy.get('[data-testid="office-psalms"]').should('be.visible')
      cy.get('[data-testid="office-prayers"]').should('be.visible')

      // But scripture sections may show errors
      cy.get('[data-testid="reading-error"]')
        .should('be.visible')
    })

    it('should not block entire page for individual component failures', () => {
      // FR-022c: Individual failures should be isolated
      
      // Only one component fails
      cy.intercept('GET', '**/api/scripture/first-reading*', {
        statusCode: 503
      }).as('firstReadingFails')

      cy.intercept('GET', '**/api/scripture/second-reading*', {
        statusCode: 200,
        body: { text: 'Second reading text' }
      }).as('secondReadingSuccess')

      cy.visit('/office/evening_prayer/2025/8/25/')

      // First reading should show error
      cy.get('[data-testid="first-reading-error"]')
        .should('be.visible')

      // Second reading should load successfully
      cy.get('[data-testid="second-reading"]')
        .should('be.visible')
        .and('contain', 'Second reading')

      // Rest of office should be intact
      cy.get('[data-testid="office-content"]')
        .should('be.visible')
    })
  })
})
