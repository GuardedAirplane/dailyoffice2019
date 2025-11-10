describe('Family Prayer Offices (US7)', () => {
  beforeEach(() => {
    cy.visit('/')
  })

  describe('Family Morning Prayer', () => {
    it('should load Family Morning Prayer office', () => {
      cy.visit('/family/family_morning_prayer/2024/3/15')
      cy.contains('Family Prayer').should('exist')
      cy.contains('Morning').should('exist')
    })

    it('should display simplified content', () => {
      cy.visit('/family/family_morning_prayer/2024/6/20')
      
      // Should have key sections but fewer than standard Morning Prayer
      cy.contains('Opening Sentence').should('exist')
      cy.contains('Psalm').should('exist')
      cy.contains('Scripture').should('exist')
      cy.contains('Lord\'s Prayer').should('exist')
    })

    it('should work with various dates', () => {
      const dates = [
        { year: 2020, month: 1, day: 1 },
        { year: 2024, month: 2, day: 29 },  // Leap year
        { year: 2050, month: 12, day: 31 },
      ]

      dates.forEach(({ year, month, day }) => {
        cy.visit(`/family/family_morning_prayer/${year}/${month}/${day}`)
        cy.contains('Family Prayer').should('exist')
        cy.contains(year.toString()).should('exist')
      })
    })

    it('should display for special liturgical dates', () => {
      // Christmas
      cy.visit('/family/family_morning_prayer/2024/12/25')
      cy.contains('Family Prayer').should('exist')
      
      // Easter
      cy.visit('/family/family_morning_prayer/2024/3/31')
      cy.contains('Family Prayer').should('exist')
    })
  })

  describe('Family Midday Prayer', () => {
    it('should load Family Midday Prayer office', () => {
      cy.visit('/family/family_midday_prayer/2024/3/15')
      cy.contains('Family Prayer').should('exist')
      cy.contains('Midday').should('exist')
    })

    it('should display simplified content', () => {
      cy.visit('/family/family_midday_prayer/2024/6/20')
      
      cy.contains('Opening Sentence').should('exist')
      cy.contains('Psalm').should('exist')
      cy.contains('Lord\'s Prayer').should('exist')
    })

    it('should work with various dates', () => {
      const dates = [
        { year: 2020, month: 1, day: 1 },
        { year: 2024, month: 7, day: 4 },
        { year: 2050, month: 9, day: 15 },
      ]

      dates.forEach(({ year, month, day }) => {
        cy.visit(`/family/family_midday_prayer/${year}/${month}/${day}`)
        cy.contains('Family Prayer').should('exist')
      })
    })
  })

  describe('Family Early Evening Prayer', () => {
    it('should load Family Early Evening Prayer office', () => {
      cy.visit('/family/family_early_evening_prayer/2024/3/15')
      cy.contains('Family Prayer').should('exist')
      cy.contains('Evening').should('exist')
    })

    it('should display simplified content', () => {
      cy.visit('/family/family_early_evening_prayer/2024/6/20')
      
      cy.contains('Opening Sentence').should('exist')
      cy.contains('Psalm').should('exist')
      cy.contains('Scripture').should('exist')
      cy.contains('Lord\'s Prayer').should('exist')
    })

    it('should work with various dates', () => {
      const dates = [
        { year: 2020, month: 1, day: 1 },
        { year: 2024, month: 8, day: 15 },
        { year: 2050, month: 11, day: 20 },
      ]

      dates.forEach(({ year, month, day }) => {
        cy.visit(`/family/family_early_evening_prayer/${year}/${month}/${day}`)
        cy.contains('Family Prayer').should('exist')
      })
    })
  })

  describe('Family Close of Day Prayer', () => {
    it('should load Family Close of Day Prayer office', () => {
      cy.visit('/family/family_close_of_day_prayer/2024/3/15')
      cy.contains('Family Prayer').should('exist')
      cy.contains('Close of Day').should('exist')
    })

    it('should display simplified content', () => {
      cy.visit('/family/family_close_of_day_prayer/2024/6/20')
      
      cy.contains('Opening Sentence').should('exist')
      cy.contains('Psalm').should('exist')
      cy.contains('Lord\'s Prayer').should('exist')
    })

    it('should work with various dates', () => {
      const dates = [
        { year: 2020, month: 1, day: 1 },
        { year: 2024, month: 10, day: 10 },
        { year: 2050, month: 5, day: 25 },
      ]

      dates.forEach(({ year, month, day }) => {
        cy.visit(`/family/family_close_of_day_prayer/${year}/${month}/${day}`)
        cy.contains('Family Prayer').should('exist')
      })
    })
  })

  describe('Family Prayer Navigation', () => {
    it('should display family offices in secondary navigation', () => {
      cy.visit('/morning_prayer/2024/3/15')
      
      // Look for family prayer navigation section
      cy.get('[data-cy="family-nav"]').should('exist')
      
      // Should list all four family offices
      cy.contains('Family Morning').should('exist')
      cy.contains('Family Midday').should('exist')
      cy.contains('Family Early Evening').should('exist')
      cy.contains('Family Close of Day').should('exist')
    })

    it('should navigate between family offices preserving date', () => {
      cy.visit('/family/family_morning_prayer/2024/5/15')
      
      // Navigate to Family Midday
      cy.get('[data-cy="nav-family-midday"]').click()
      cy.url().should('include', '/family/family_midday_prayer/2024/5/15')
      
      // Navigate to Family Evening
      cy.get('[data-cy="nav-family-evening"]').click()
      cy.url().should('include', '/family/family_early_evening_prayer/2024/5/15')
      
      // Navigate to Family Close of Day
      cy.get('[data-cy="nav-family-close"]').click()
      cy.url().should('include', '/family/family_close_of_day_prayer/2024/5/15')
    })

    it('should allow switching from standard to family offices', () => {
      cy.visit('/morning_prayer/2024/7/4')
      
      // Click link to family morning prayer
      cy.get('[data-cy="family-morning-link"]').click()
      cy.url().should('include', '/family/family_morning_prayer/2024/7/4')
    })

    it('should allow switching from family to standard offices', () => {
      cy.visit('/family/family_morning_prayer/2024/7/4')
      
      // Click link to standard morning prayer
      cy.get('[data-cy="standard-morning-link"]').click()
      cy.url().should('include', '/morning_prayer/2024/7/4')
    })

    it('should preserve date when switching between office types', () => {
      const testDate = '2024/9/15'
      
      cy.visit(`/family/family_morning_prayer/${testDate}`)
      cy.get('[data-cy="nav-family-midday"]').click()
      cy.url().should('include', testDate)
      
      cy.get('[data-cy="nav-family-evening"]').click()
      cy.url().should('include', testDate)
    })

    it('should show family offices as separate from standard offices', () => {
      cy.visit('/morning_prayer/2024/3/15')
      
      // Family section should be visually distinct
      cy.get('[data-cy="family-nav"]').should('have.class', 'family-section')
      
      // Or be in a separate navigation group
      cy.get('[data-cy="family-nav"]').parent().should('not.have.class', 'standard-nav')
    })
  })

  describe('Family Prayer Date Navigation', () => {
    it('should navigate to previous day in family office', () => {
      cy.visit('/family/family_morning_prayer/2024/3/15')
      cy.get('[data-cy="previous-day"]').click()
      cy.url().should('include', '/2024/3/14')
    })

    it('should navigate to next day in family office', () => {
      cy.visit('/family/family_midday_prayer/2024/3/15')
      cy.get('[data-cy="next-day"]').click()
      cy.url().should('include', '/2024/3/16')
    })

    it('should handle month boundaries in family offices', () => {
      cy.visit('/family/family_early_evening_prayer/2024/3/31')
      cy.get('[data-cy="next-day"]').click()
      cy.url().should('include', '/2024/4/1')
    })

    it('should handle year boundaries in family offices', () => {
      cy.visit('/family/family_close_of_day_prayer/2024/12/31')
      cy.get('[data-cy="next-day"]').click()
      cy.url().should('include', '/2025/1/1')
    })
  })

  describe('Family Prayer Content Validation', () => {
    it('should show appropriate content for children/families', () => {
      cy.visit('/family/family_morning_prayer/2024/6/15')
      
      // Should not have complex rubrics or multiple readings
      cy.get('.complex-rubric').should('not.exist')
      
      // Should have simpler, family-friendly content
      cy.contains('Lord\'s Prayer').should('exist')
    })

    it('should display collect of the day', () => {
      cy.visit('/family/family_morning_prayer/2024/7/20')
      cy.contains('Collect').should('exist')
    })

    it('should include psalms', () => {
      cy.visit('/family/family_midday_prayer/2024/8/10')
      cy.contains('Psalm').should('exist')
    })

    it('should include scripture readings', () => {
      cy.visit('/family/family_early_evening_prayer/2024/9/5')
      cy.contains('Scripture').should('exist')
    })

    it('should include prayers appropriate for families', () => {
      cy.visit('/family/family_close_of_day_prayer/2024/10/15')
      cy.contains(/Prayer|Intercession/).should('exist')
    })
  })

  describe('Family Prayer Accessibility', () => {
    it('should have clear headings for screen readers', () => {
      cy.visit('/family/family_morning_prayer/2024/5/20')
      
      cy.get('h1').should('exist')
      cy.get('h2').should('exist')
    })

    it('should be keyboard navigable', () => {
      cy.visit('/family/family_morning_prayer/2024/5/20')
      
      cy.get('body').tab()
      cy.focused().should('exist')
    })

    it('should have appropriate ARIA labels', () => {
      cy.visit('/family/family_morning_prayer/2024/5/20')
      
      cy.get('[data-cy="family-nav"]').should('have.attr', 'aria-label')
    })
  })

  describe('Family Prayer Mobile Experience', () => {
    it('should be responsive on mobile devices', () => {
      cy.viewport('iphone-x')
      cy.visit('/family/family_morning_prayer/2024/6/15')
      
      cy.contains('Family Prayer').should('be.visible')
    })

    it('should have touch-friendly navigation on mobile', () => {
      cy.viewport('iphone-x')
      cy.visit('/family/family_midday_prayer/2024/7/10')
      
      // Navigation buttons should be large enough for touch
      cy.get('[data-cy="next-day"]').should('have.css', 'min-height')
    })

    it('should collapse navigation on small screens', () => {
      cy.viewport('iphone-6')
      cy.visit('/family/family_early_evening_prayer/2024/8/5')
      
      // Mobile menu should exist
      cy.get('[data-cy="mobile-menu-toggle"]').should('exist')
    })
  })

  describe('Family Prayer for Special Occasions', () => {
    it('should work correctly on Christmas', () => {
      cy.visit('/family/family_morning_prayer/2024/12/25')
      cy.contains('Family Prayer').should('exist')
      cy.contains(/Christmas|Nativity/).should('exist')
    })

    it('should work correctly on Easter', () => {
      cy.visit('/family/family_morning_prayer/2024/3/31')
      cy.contains('Family Prayer').should('exist')
      cy.contains(/Easter/).should('exist')
    })

    it('should work correctly on Ash Wednesday', () => {
      cy.visit('/family/family_morning_prayer/2024/2/14')
      cy.contains('Family Prayer').should('exist')
      cy.contains(/Ash Wednesday|Lent/).should('exist')
    })
  })

  describe('Family Prayer URL Patterns', () => {
    it('should use /family/ prefix in URLs', () => {
      cy.visit('/family/family_morning_prayer/2024/5/15')
      cy.url().should('include', '/family/')
    })

    it('should maintain URL pattern consistency across all family offices', () => {
      const offices = [
        'family_morning_prayer',
        'family_midday_prayer',
        'family_early_evening_prayer',
        'family_close_of_day_prayer',
      ]

      offices.forEach(office => {
        cy.visit(`/family/${office}/2024/6/15`)
        cy.url().should('include', '/family/')
        cy.url().should('include', office)
      })
    })

    it('should handle direct URL access to family offices', () => {
      cy.visit('/family/family_early_evening_prayer/2024/9/20')
      cy.contains('Family Prayer').should('exist')
      cy.contains('Early Evening').should('exist')
    })
  })
})
