describe('Major BCP 2019 Feasts (Phase 10)', () => {
  describe('Christmas (December 25)', () => {
    it('should display Christmas Day Morning Prayer', () => {
      cy.visit('/morning_prayer/2024/12/25')
      cy.contains(/Christmas|Nativity/).should('exist')
      cy.contains('2024').should('exist')
    })

    it('should display Christmas Day Evening Prayer', () => {
      cy.visit('/evening_prayer/2024/12/25')
      cy.contains(/Christmas|Nativity/).should('exist')
    })

    it('should show Christmastide season', () => {
      cy.visit('/morning_prayer/2024/12/25')
      cy.contains(/Christmastide/).should('exist')
    })

    it('should display Christmas across multiple years', () => {
      cy.visit('/morning_prayer/2025/12/25')
      cy.contains(/Christmas|Nativity/).should('exist')
    })
  })

  describe('Easter Day (Movable Feast)', () => {
    it('should display Easter 2024 (March 31)', () => {
      cy.visit('/morning_prayer/2024/3/31')
      cy.contains(/Easter/).should('exist')
      cy.contains('2024').should('exist')
    })

    it('should display Easter 2025 (April 20)', () => {
      cy.visit('/morning_prayer/2025/4/20')
      cy.contains(/Easter/).should('exist')
      cy.contains('2025').should('exist')
    })

    it('should show Eastertide season', () => {
      cy.visit('/evening_prayer/2024/3/31')
      cy.contains(/Eastertide|Easter/).should('exist')
    })

    it('should extend Eastertide beyond Easter Day', () => {
      cy.visit('/morning_prayer/2024/4/7')  // Week after Easter
      cy.contains(/Eastertide|Easter/).should('exist')
    })
  })

  describe('Epiphany (January 6)', () => {
    it('should display Epiphany Morning Prayer', () => {
      cy.visit('/morning_prayer/2024/1/6')
      cy.contains(/Epiphany/).should('exist')
    })

    it('should display Epiphany Evening Prayer', () => {
      cy.visit('/evening_prayer/2024/1/6')
      cy.contains(/Epiphany/).should('exist')
    })

    it('should be consistent across years', () => {
      cy.visit('/morning_prayer/2025/1/6')
      cy.contains(/Epiphany/).should('exist')
    })
  })

  describe('Ascension Day (40 days after Easter)', () => {
    it('should display Ascension 2024 (May 9)', () => {
      cy.visit('/morning_prayer/2024/5/9')
      cy.contains(/Ascension/).should('exist')
    })

    it('should display Ascension 2025 (May 29)', () => {
      cy.visit('/morning_prayer/2025/5/29')
      cy.contains(/Ascension/).should('exist')
    })

    it('should show in Evening Prayer', () => {
      cy.visit('/evening_prayer/2024/5/9')
      cy.contains(/Ascension/).should('exist')
    })
  })

  describe('Pentecost (50 days after Easter)', () => {
    it('should display Pentecost 2024 (May 19)', () => {
      cy.visit('/morning_prayer/2024/5/19')
      cy.contains(/Pentecost/).should('exist')
    })

    it('should display Pentecost 2025 (June 8)', () => {
      cy.visit('/morning_prayer/2025/6/8')
      cy.contains(/Pentecost/).should('exist')
    })

    it('should show Season After Pentecost begins', () => {
      cy.visit('/evening_prayer/2024/5/19')
      cy.contains(/Pentecost|Season After Pentecost/).should('exist')
    })

    it('should show in all office types', () => {
      cy.visit('/midday_prayer/2024/5/19')
      cy.contains(/Pentecost/).should('exist')
      
      cy.visit('/compline/2024/5/19')
      cy.contains(/Pentecost/).should('exist')
    })
  })

  describe('Trinity Sunday (Sunday after Pentecost)', () => {
    it('should display Trinity Sunday 2024 (May 26)', () => {
      cy.visit('/morning_prayer/2024/5/26')
      cy.contains(/Trinity/).should('exist')
    })

    it('should display Trinity Sunday 2025 (June 15)', () => {
      cy.visit('/morning_prayer/2025/6/15')
      cy.contains(/Trinity/).should('exist')
    })

    it('should show in Evening Prayer', () => {
      cy.visit('/evening_prayer/2024/5/26')
      cy.contains(/Trinity/).should('exist')
    })
  })

  describe('All Saints\' Day (November 1)', () => {
    it('should display All Saints Morning Prayer', () => {
      cy.visit('/morning_prayer/2024/11/1')
      cy.contains(/All Saints/).should('exist')
    })

    it('should display All Saints Evening Prayer', () => {
      cy.visit('/evening_prayer/2024/11/1')
      cy.contains(/All Saints/).should('exist')
    })

    it('should be consistent across years', () => {
      cy.visit('/morning_prayer/2025/11/1')
      cy.contains(/All Saints/).should('exist')
      
      cy.visit('/morning_prayer/2023/11/1')
      cy.contains(/All Saints/).should('exist')
    })

    it('should appear in all office types', () => {
      cy.visit('/midday_prayer/2024/11/1')
      cy.contains(/All Saints/).should('exist')
    })
  })

  describe('Ash Wednesday (46 days before Easter)', () => {
    it('should display Ash Wednesday 2024 (February 14)', () => {
      cy.visit('/morning_prayer/2024/2/14')
      cy.contains(/Ash Wednesday|Lent/).should('exist')
    })

    it('should display Ash Wednesday 2025 (March 5)', () => {
      cy.visit('/morning_prayer/2025/3/5')
      cy.contains(/Ash Wednesday|Lent/).should('exist')
    })

    it('should mark beginning of Lent', () => {
      cy.visit('/evening_prayer/2024/2/14')
      cy.contains(/Lent|Ash Wednesday/).should('exist')
    })

    it('should show day before is not Lent', () => {
      // Day before Ash Wednesday
      cy.visit('/morning_prayer/2024/2/13')
      // Should not be in Lent yet
      cy.contains(/Epiphanytide|Epiphany/).should('exist')
    })
  })

  describe('Palm Sunday (Sunday before Easter)', () => {
    it('should display Palm Sunday 2024 (March 24)', () => {
      cy.visit('/morning_prayer/2024/3/24')
      cy.contains(/Palm Sunday|Holy Week/).should('exist')
    })

    it('should display Palm Sunday 2025 (April 13)', () => {
      cy.visit('/morning_prayer/2025/4/13')
      cy.contains(/Palm Sunday|Holy Week/).should('exist')
    })

    it('should mark beginning of Holy Week', () => {
      cy.visit('/evening_prayer/2024/3/24')
      cy.contains(/Holy Week|Palm/).should('exist')
    })
  })

  describe('Good Friday (Friday before Easter)', () => {
    it('should display Good Friday 2024 (March 29)', () => {
      cy.visit('/morning_prayer/2024/3/29')
      cy.contains(/Good Friday|Holy Week/).should('exist')
    })

    it('should display Good Friday 2025 (April 18)', () => {
      cy.visit('/morning_prayer/2025/4/18')
      cy.contains(/Good Friday|Holy Week/).should('exist')
    })

    it('should be in Holy Week season', () => {
      cy.visit('/evening_prayer/2024/3/29')
      cy.contains(/Holy Week|Good Friday/).should('exist')
    })

    it('should show across all office types', () => {
      cy.visit('/midday_prayer/2024/3/29')
      cy.contains(/Good Friday|Holy Week/).should('exist')
      
      cy.visit('/compline/2024/3/29')
      cy.contains(/Holy Week/).should('exist')
    })
  })

  describe('Feast Day Navigation', () => {
    it('should navigate between feast day offices', () => {
      cy.visit('/morning_prayer/2024/12/25')  // Christmas
      
      cy.get('[data-cy="nav-evening"]').click()
      cy.url().should('include', '/evening_prayer/2024/12/25')
      cy.contains(/Christmas|Nativity/).should('exist')
    })

    it('should navigate to next day from feast', () => {
      cy.visit('/morning_prayer/2024/12/25')  // Christmas
      
      cy.get('[data-cy="next-day"]').click()
      cy.url().should('include', '/2024/12/26')
      // St. Stephen's Day
      cy.contains(/Stephen|Christmastide/).should('exist')
    })

    it('should navigate to previous day to feast', () => {
      cy.visit('/morning_prayer/2024/12/26')
      
      cy.get('[data-cy="previous-day"]').click()
      cy.url().should('include', '/2024/12/25')
      cy.contains(/Christmas|Nativity/).should('exist')
    })
  })

  describe('Feast Day Content Validation', () => {
    it('should display appropriate psalms for feasts', () => {
      cy.visit('/morning_prayer/2024/12/25')
      cy.contains(/Psalm/).should('exist')
    })

    it('should display scripture readings for feasts', () => {
      cy.visit('/morning_prayer/2024/3/31')  // Easter
      cy.contains(/Scripture|Reading/).should('exist')
    })

    it('should display collects for feasts', () => {
      cy.visit('/evening_prayer/2024/12/25')
      cy.contains(/Collect/).should('exist')
    })

    it('should show commemorations prominently', () => {
      cy.visit('/morning_prayer/2024/11/1')  // All Saints
      cy.contains(/All Saints/).should('be.visible')
    })
  })

  describe('Liturgical Seasons Through Feasts', () => {
    it('should show Advent season', () => {
      cy.visit('/morning_prayer/2024/12/1')  // First Sunday of Advent
      cy.contains(/Advent/).should('exist')
    })

    it('should transition from Advent to Christmastide', () => {
      // Day before Christmas
      cy.visit('/morning_prayer/2024/12/24')
      cy.contains(/Advent/).should('exist')
      
      // Christmas Day
      cy.visit('/morning_prayer/2024/12/25')
      cy.contains(/Christmastide/).should('exist')
    })

    it('should show Lent season during Ash Wednesday', () => {
      cy.visit('/evening_prayer/2024/2/14')
      cy.contains(/Lent/).should('exist')
    })

    it('should show Holy Week season', () => {
      cy.visit('/morning_prayer/2024/3/28')  // Maundy Thursday
      cy.contains(/Holy Week/).should('exist')
    })

    it('should transition from Holy Week to Eastertide', () => {
      // Holy Saturday
      cy.visit('/morning_prayer/2024/3/30')
      cy.contains(/Holy Week/).should('exist')
      
      // Easter Day
      cy.visit('/morning_prayer/2024/3/31')
      cy.contains(/Eastertide/).should('exist')
    })

    it('should show Season After Pentecost', () => {
      cy.visit('/morning_prayer/2024/7/15')
      cy.contains(/Season After Pentecost|Pentecost/).should('exist')
    })
  })

  describe('Feast Day Consistency', () => {
    it('should show same feast in family prayer', () => {
      cy.visit('/family/family_morning_prayer/2024/12/25')
      cy.contains(/Christmas|Nativity/).should('exist')
    })

    it('should preserve feast commemoration across office types', () => {
      const offices = [
        '/morning_prayer',
        '/midday_prayer',
        '/evening_prayer',
        '/compline'
      ]

      offices.forEach(office => {
        cy.visit(`${office}/2024/12/25`)
        cy.contains(/Christmas|Nativity|Christmastide/).should('exist')
      })
    })

    it('should show feasts in past years', () => {
      cy.visit('/morning_prayer/2020/12/25')
      cy.contains(/Christmas|Nativity/).should('exist')
    })

    it('should show feasts in future years', () => {
      cy.visit('/morning_prayer/2030/12/25')
      cy.contains(/Christmas|Nativity/).should('exist')
    })
  })

  describe('Mobile Feast Handling', () => {
    it('should handle Easter calculation for various years', () => {
      const easterDates = [
        { year: 2024, month: 3, day: 31 },
        { year: 2025, month: 4, day: 20 },
        { year: 2026, month: 4, day: 5 },
      ]

      easterDates.forEach(({ year, month, day }) => {
        cy.visit(`/morning_prayer/${year}/${month}/${day}`)
        cy.contains(/Easter/).should('exist')
      })
    })

    it('should calculate Ash Wednesday correctly', () => {
      const ashWednesdayDates = [
        { year: 2024, month: 2, day: 14 },
        { year: 2025, month: 3, day: 5 },
        { year: 2026, month: 2, day: 18 },
      ]

      ashWednesdayDates.forEach(({ year, month, day }) => {
        cy.visit(`/morning_prayer/${year}/${month}/${day}`)
        cy.contains(/Ash Wednesday|Lent/).should('exist')
      })
    })

    it('should calculate Ascension correctly', () => {
      const ascensionDates = [
        { year: 2024, month: 5, day: 9 },
        { year: 2025, month: 5, day: 29 },
        { year: 2026, month: 5, day: 14 },
      ]

      ascensionDates.forEach(({ year, month, day }) => {
        cy.visit(`/morning_prayer/${year}/${month}/${day}`)
        cy.contains(/Ascension/).should('exist')
      })
    })
  })

  describe('Fixed Feast Consistency', () => {
    it('should show Epiphany on same date every year', () => {
      const years = [2024, 2025, 2026, 2030]
      
      years.forEach(year => {
        cy.visit(`/morning_prayer/${year}/1/6`)
        cy.contains(/Epiphany/).should('exist')
      })
    })

    it('should show All Saints on same date every year', () => {
      const years = [2024, 2025, 2026, 2030]
      
      years.forEach(year => {
        cy.visit(`/morning_prayer/${year}/11/1`)
        cy.contains(/All Saints/).should('exist')
      })
    })

    it('should show Christmas on same date every year', () => {
      const years = [2024, 2025, 2026, 2030]
      
      years.forEach(year => {
        cy.visit(`/morning_prayer/${year}/12/25`)
        cy.contains(/Christmas|Nativity/).should('exist')
      })
    })
  })
})
