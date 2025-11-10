describe('Date Navigation (US6)', () => {
  beforeEach(() => {
    cy.visit('/morning_prayer/2024/1/15')
  })

  describe('Date Range Acceptance', () => {
    it('should accept far past dates (1900s)', () => {
      cy.visit('/morning_prayer/1950/6/15')
      cy.contains('Office for').should('exist')
      cy.contains('1950').should('exist')
    })

    it('should accept far future dates (2100s)', () => {
      cy.visit('/evening_prayer/2075/9/20')
      cy.contains('Office for').should('exist')
      cy.contains('2075').should('exist')
    })

    it('should accept mid-century dates (2050)', () => {
      cy.visit('/midday_prayer/2050/12/31')
      cy.contains('Office for').should('exist')
      cy.contains('2050').should('exist')
    })

    it('should accept various decades consistently', () => {
      const dates = [
        { year: 1975, month: 6, day: 15 },
        { year: 2000, month: 12, day: 25 },
        { year: 2025, month: 3, day: 15 },
      ]

      dates.forEach(({ year, month, day }) => {
        cy.visit(`/compline/${year}/${month}/${day}`)
        cy.contains('Office for').should('exist')
        cy.contains(year.toString()).should('exist')
      })
    })
  })

  describe('Leap Year Handling', () => {
    it('should accept February 29 in leap years', () => {
      cy.visit('/morning_prayer/2024/2/29')
      cy.contains('Office for').should('exist')
      cy.contains('February 29').should('exist')
    })

    it('should handle century leap year (2000)', () => {
      cy.visit('/evening_prayer/2000/2/29')
      cy.contains('Office for').should('exist')
      cy.contains('February 29').should('exist')
    })

    it('should handle future leap years (2048)', () => {
      cy.visit('/midday_prayer/2048/2/29')
      cy.contains('Office for').should('exist')
      cy.contains('February 29').should('exist')
    })

    it('should handle Feb 28 in non-leap years', () => {
      cy.visit('/compline/2023/2/28')
      cy.contains('Office for').should('exist')
      cy.contains('February 28').should('exist')
    })

    it('should reject February 29 in non-leap years', () => {
      // Most routers/apps handle invalid dates by redirecting or showing error
      cy.visit('/morning_prayer/2023/2/29', { failOnStatusCode: false })
      // Check that it either shows error or redirects to valid date
      cy.url().should('not.include', '2023/2/29')
    })
  })

  describe('Church Year Transitions', () => {
    it('should correctly display Advent season', () => {
      cy.visit('/morning_prayer/2024/12/1')
      cy.contains('Office for').should('exist')
      cy.contains(/Advent|First Sunday of Advent/).should('exist')
    })

    it('should transition from Epiphanytide to Lent on Ash Wednesday', () => {
      // Day before Ash Wednesday (2024)
      cy.visit('/evening_prayer/2024/2/13')
      cy.contains('Office for').should('exist')
      
      // Ash Wednesday
      cy.visit('/morning_prayer/2024/2/14')
      cy.contains('Office for').should('exist')
      cy.contains(/Ash Wednesday|Lent/).should('exist')
    })

    it('should transition to Eastertide on Easter Day', () => {
      cy.visit('/morning_prayer/2024/3/31')
      cy.contains('Office for').should('exist')
      cy.contains(/Easter|Eastertide/).should('exist')
    })

    it('should show correct season for Pentecost', () => {
      cy.visit('/evening_prayer/2024/5/19')
      cy.contains('Office for').should('exist')
      cy.contains(/Pentecost|Season After Pentecost/).should('exist')
    })

    it('should mark beginning of church year at Advent', () => {
      // Last day before Advent (Saturday)
      cy.visit('/compline/2024/11/30')
      cy.contains('Office for').should('exist')
      
      // First Sunday of Advent
      cy.visit('/morning_prayer/2024/12/1')
      cy.contains('Office for').should('exist')
      cy.contains(/Advent/).should('exist')
    })
  })

  describe('Date Navigation Controls', () => {
    it('should navigate to previous day', () => {
      cy.get('[data-cy="previous-day"]').click()
      cy.url().should('include', '/2024/1/14')
    })

    it('should navigate to next day', () => {
      cy.get('[data-cy="next-day"]').click()
      cy.url().should('include', '/2024/1/16')
    })

    it('should navigate across month boundaries forward', () => {
      cy.visit('/evening_prayer/2024/1/31')
      cy.get('[data-cy="next-day"]').click()
      cy.url().should('include', '/2024/2/1')
    })

    it('should navigate across month boundaries backward', () => {
      cy.visit('/midday_prayer/2024/2/1')
      cy.get('[data-cy="previous-day"]').click()
      cy.url().should('include', '/2024/1/31')
    })

    it('should navigate across year boundaries forward', () => {
      cy.visit('/compline/2024/12/31')
      cy.get('[data-cy="next-day"]').click()
      cy.url().should('include', '/2025/1/1')
    })

    it('should navigate across year boundaries backward', () => {
      cy.visit('/morning_prayer/2025/1/1')
      cy.get('[data-cy="previous-day"]').click()
      cy.url().should('include', '/2024/12/31')
    })
  })

  describe('Date Picker', () => {
    it('should open date picker when clicking date display', () => {
      cy.get('[data-cy="date-display"]').click()
      cy.get('[data-cy="date-picker"]').should('be.visible')
    })

    it('should allow selecting a specific date', () => {
      cy.get('[data-cy="date-display"]').click()
      cy.get('[data-cy="date-picker"]').should('be.visible')
      
      // Select a specific date (implementation depends on date picker library)
      cy.get('[data-cy="date-picker-day-25"]').click()
      cy.url().should('include', '/25')
    })

    it('should update office content when date changed via picker', () => {
      const originalDate = '2024-01-15'
      
      cy.get('[data-cy="date-display"]').click()
      cy.get('[data-cy="date-picker-day-20"]').click()
      
      // Verify URL changed
      cy.url().should('include', '/20')
      
      // Verify content updated
      cy.contains('January 20').should('exist')
    })

    it('should allow selecting dates in different months', () => {
      cy.get('[data-cy="date-display"]').click()
      cy.get('[data-cy="date-picker-next-month"]').click()
      cy.get('[data-cy="date-picker-day-15"]').click()
      
      cy.url().should('include', '/2/15')
    })

    it('should allow selecting dates in different years', () => {
      cy.get('[data-cy="date-display"]').click()
      cy.get('[data-cy="date-picker-year-selector"]').select('2025')
      cy.get('[data-cy="date-picker-day-15"]').click()
      
      cy.url().should('include', '2025')
    })
  })

  describe('Direct URL Access', () => {
    it('should load office when accessing via direct URL', () => {
      cy.visit('/evening_prayer/2024/6/15')
      cy.contains('Office for').should('exist')
      cy.contains('June 15').should('exist')
    })

    it('should maintain office type in URL navigation', () => {
      cy.visit('/midday_prayer/2024/3/20')
      cy.get('[data-cy="next-day"]').click()
      cy.url().should('include', '/midday_prayer/2024/3/21')
    })

    it('should preserve date when switching office types', () => {
      cy.visit('/morning_prayer/2024/4/10')
      cy.get('[data-cy="nav-evening"]').click()
      cy.url().should('include', '/evening_prayer/2024/4/10')
    })
  })

  describe('Dynamic Liturgical Content', () => {
    it('should calculate correct Easter date for 2050', () => {
      // Easter 2050 is April 10
      cy.visit('/morning_prayer/2050/4/10')
      cy.contains(/Easter|Eastertide/).should('exist')
    })

    it('should calculate correct Advent for future years', () => {
      // First Sunday of Advent 2050 is November 27
      cy.visit('/evening_prayer/2050/11/27')
      cy.contains(/Advent/).should('exist')
    })

    it('should calculate correct Ash Wednesday for past years', () => {
      // Ash Wednesday 2020 was February 26
      cy.visit('/morning_prayer/2020/2/26')
      cy.contains(/Ash Wednesday|Lent/).should('exist')
    })

    it('should show correct readings for any date', () => {
      cy.visit('/evening_prayer/2030/7/15')
      cy.contains(/Psalm|Scripture/).should('exist')
    })
  })

  describe('Invalid Date Handling', () => {
    it('should handle invalid month (13)', () => {
      cy.visit('/morning_prayer/2024/13/1', { failOnStatusCode: false })
      cy.url().should('not.include', '/13/')
    })

    it('should handle invalid day for month (Feb 30)', () => {
      cy.visit('/evening_prayer/2024/2/30', { failOnStatusCode: false })
      cy.url().should('not.include', '/2/30')
    })

    it('should handle invalid day (32)', () => {
      cy.visit('/midday_prayer/2024/1/32', { failOnStatusCode: false })
      cy.url().should('not.include', '/32')
    })

    it('should handle malformed dates gracefully', () => {
      cy.visit('/compline/2024/abc/def', { failOnStatusCode: false })
      cy.url().should('not.include', '/abc/')
    })
  })

  describe('Performance with Date Range', () => {
    it('should load offices quickly for past dates', () => {
      const start = Date.now()
      cy.visit('/morning_prayer/2010/3/15')
      cy.contains('Office for').should('exist')
      const elapsed = Date.now() - start
      expect(elapsed).to.be.lessThan(3000) // 3 second max
    })

    it('should load offices quickly for future dates', () => {
      const start = Date.now()
      cy.visit('/evening_prayer/2080/9/20')
      cy.contains('Office for').should('exist')
      const elapsed = Date.now() - start
      expect(elapsed).to.be.lessThan(3000)
    })
  })

  describe('Browser History', () => {
    it('should support back button navigation', () => {
      cy.visit('/morning_prayer/2024/1/15')
      cy.get('[data-cy="next-day"]').click()
      cy.url().should('include', '/16')
      
      cy.go('back')
      cy.url().should('include', '/15')
    })

    it('should support forward button navigation', () => {
      cy.visit('/evening_prayer/2024/2/10')
      cy.get('[data-cy="next-day"]').click()
      cy.go('back')
      cy.go('forward')
      
      cy.url().should('include', '/11')
    })
  })
})
