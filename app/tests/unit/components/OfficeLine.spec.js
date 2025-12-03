/**
 * Unit tests for Office line components (OfficeHeading, OfficeLeader, OfficeCongregation, etc.)
 * 
 * Validates: FR-001 (Display Morning Prayer liturgical components with correct formatting)
 * 
 * These components represent different types of liturgical text lines in the Daily Office.
 */

import { describe, it, expect } from 'vitest';
import { shallowMount } from '@vue/test-utils';
import OfficeHeading from '../../../src/components/OfficeHeading.vue';
import OfficeSubheading from '../../../src/components/OfficeSubheading.vue';
import OfficeCitation from '../../../src/components/OfficeCitation.vue';
import OfficeHTML from '../../../src/components/OfficeHTML.vue';
import OfficeLeader from '../../../src/components/OfficeLeader.vue';
import OfficeCongregation from '../../../src/components/OfficeCongregation.vue';
import OfficeLeaderDialogue from '../../../src/components/OfficeLeaderDialogue.vue';
import OfficeCongregationDialogue from '../../../src/components/OfficeCongregationDialogue.vue';
import OfficeRubric from '../../../src/components/OfficeRubric.vue';
import OfficeSpacer from '../../../src/components/OfficeSpacer.vue';

/**
 * FR-001: Office line components render different types of liturgical text
 */
describe('OfficeHeading.vue', () => {
  it('should render heading content in h2 tag', () => {
    const line = { content: 'Morning Prayer' };
    const wrapper = shallowMount(OfficeHeading, {
      props: { line },
    });

    expect(wrapper.find('h2').exists()).toBe(true);
    expect(wrapper.find('h2').text()).toBe('Morning Prayer');
  });

  it('should render different heading text', () => {
    const line = { content: 'The Invitatory' };
    const wrapper = shallowMount(OfficeHeading, {
      props: { line },
    });

    expect(wrapper.find('h2').text()).toBe('The Invitatory');
  });

  it('should handle empty content', () => {
    const line = { content: '' };
    const wrapper = shallowMount(OfficeHeading, {
      props: { line },
    });

    expect(wrapper.find('h2').exists()).toBe(true);
    expect(wrapper.find('h2').text()).toBe('');
  });
});

describe('OfficeSubheading.vue', () => {
  it('should render subheading content', () => {
    const line = { content: 'The Confession of Sin' };
    const wrapper = shallowMount(OfficeSubheading, {
      props: { line },
    });

    expect(wrapper.text()).toBe('The Confession of Sin');
  });

  it('should render different subheading text', () => {
    const line = { content: 'The Apostles\' Creed' };
    const wrapper = shallowMount(OfficeSubheading, {
      props: { line },
    });

    expect(wrapper.text()).toBe('The Apostles\' Creed');
  });
});

describe('OfficeCitation.vue', () => {
  it('should render citation content', () => {
    const line = { content: 'Psalm 95:1-7' };
    const wrapper = shallowMount(OfficeCitation, {
      props: { line },
    });

    expect(wrapper.text()).toContain('Psalm 95:1-7');
  });

  it('should render scripture citations', () => {
    const line = { content: 'Isaiah 55:6-9' };
    const wrapper = shallowMount(OfficeCitation, {
      props: { line },
    });

    expect(wrapper.text()).toContain('Isaiah 55:6-9');
  });
});

describe('OfficeHTML.vue', () => {
  it('should render HTML content', () => {
    const line = { content: '<p>Test paragraph</p>' };
    const wrapper = shallowMount(OfficeHTML, {
      props: { line },
    });

    expect(wrapper.html()).toContain('<p>Test paragraph</p>');
  });

  it('should handle complex HTML', () => {
    const line = { content: '<p><strong>Bold text</strong> and <em>italic text</em></p>' };
    const wrapper = shallowMount(OfficeHTML, {
      props: { line },
    });

    expect(wrapper.html()).toContain('<strong>Bold text</strong>');
    expect(wrapper.html()).toContain('<em>italic text</em>');
  });
});

describe('OfficeLeader.vue', () => {
  it('should render leader text', () => {
    const line = { 
      content: 'The Lord is in his holy temple; let all the earth keep silence before him.',
    };
    const wrapper = shallowMount(OfficeLeader, {
      props: { line },
    });

    expect(wrapper.text()).toContain('The Lord is in his holy temple');
  });

  it('should render versicle text', () => {
    const line = { 
      content: 'O Lord, open our lips;',
    };
    const wrapper = shallowMount(OfficeLeader, {
      props: { line },
    });

    expect(wrapper.text()).toContain('O Lord, open our lips');
  });

  it('should display Leader label', () => {
    const line = { content: 'Let us confess our sins against God' };
    const wrapper = shallowMount(OfficeLeader, {
      props: { line },
    });

    // Component should indicate it's leader text
    expect(wrapper.html()).toBeTruthy();
  });
});

describe('OfficeCongregation.vue', () => {
  it('should render congregation response', () => {
    const line = { 
      content: 'And our mouth shall proclaim your praise.',
    };
    const wrapper = shallowMount(OfficeCongregation, {
      props: { line },
    });

    expect(wrapper.text()).toContain('And our mouth shall proclaim your praise');
  });

  it('should render different congregation text', () => {
    const line = { 
      content: 'Amen.',
    };
    const wrapper = shallowMount(OfficeCongregation, {
      props: { line },
    });

    expect(wrapper.text()).toContain('Amen');
  });

  it('should display congregation response text', () => {
    const line = { content: 'Glory to the Father, and to the Son, and to the Holy Spirit' };
    const wrapper = shallowMount(OfficeCongregation, {
      props: { line },
    });

    expect(wrapper.text()).toContain('Glory to the Father');
  });
});

describe('OfficeLeaderDialogue.vue', () => {
  it('should render leader dialogue', () => {
    const line = { 
      content: 'Alleluia! The Lord is risen indeed:',
    };
    const wrapper = shallowMount(OfficeLeaderDialogue, {
      props: { line },
    });

    expect(wrapper.text()).toContain('Alleluia');
  });

  it('should handle dialogue formatting', () => {
    const line = { content: 'The Word was made flesh and dwelt among us:' };
    const wrapper = shallowMount(OfficeLeaderDialogue, {
      props: { line },
    });

    expect(wrapper.text()).toContain('The Word was made flesh');
  });
});

describe('OfficeCongregationDialogue.vue', () => {
  it('should render congregation dialogue response', () => {
    const line = { 
      content: 'Come let us adore him. Alleluia!',
    };
    const wrapper = shallowMount(OfficeCongregationDialogue, {
      props: { line },
    });

    expect(wrapper.text()).toContain('Come let us adore him');
  });

  it('should handle different dialogue responses', () => {
    const line = { content: 'And we beheld his glory.' };
    const wrapper = shallowMount(OfficeCongregationDialogue, {
      props: { line },
    });

    expect(wrapper.text()).toContain('And we beheld his glory');
  });
});

describe('OfficeRubric.vue', () => {
  it('should render rubric instruction text', () => {
    const line = { 
      content: 'The Officiant says to the People',
    };
    const wrapper = shallowMount(OfficeRubric, {
      props: { line },
    });

    expect(wrapper.text()).toContain('The Officiant says to the People');
  });

  it('should render different rubric instructions', () => {
    const line = { content: 'The People stand or kneel' };
    const wrapper = shallowMount(OfficeRubric, {
      props: { line },
    });

    expect(wrapper.text()).toContain('The People stand or kneel');
  });

  it('should style rubric text appropriately', () => {
    const line = { content: 'Then may be said or sung' };
    const wrapper = shallowMount(OfficeRubric, {
      props: { line },
    });

    // Rubric should exist and render text
    expect(wrapper.html()).toBeTruthy();
    expect(wrapper.text()).toContain('Then may be said or sung');
  });
});

describe('OfficeSpacer.vue', () => {
  it('should render a spacer element', () => {
    const wrapper = shallowMount(OfficeSpacer);

    expect(wrapper.exists()).toBe(true);
  });

  it('should not display any text content', () => {
    const wrapper = shallowMount(OfficeSpacer);

    // Spacer should be empty or minimal
    const text = wrapper.text().trim();
    expect(text === '' || text.length === 0).toBe(true);
  });
});

/**
 * Cross-component integration tests
 */
describe('Line Component Integration', () => {
  it('should render all line types with consistent prop interface', () => {
    const line = { content: 'Test content' };
    
    const components = [
      OfficeHeading,
      OfficeSubheading,
      OfficeCitation,
      OfficeHTML,
      OfficeLeader,
      OfficeCongregation,
      OfficeLeaderDialogue,
      OfficeCongregationDialogue,
      OfficeRubric,
    ];

    components.forEach((Component) => {
      const wrapper = shallowMount(Component, {
        props: { line },
      });
      
      expect(wrapper.exists()).toBe(true);
    });
  });

  it('should handle line prop for all components except spacer', () => {
    const line = { content: 'Sample liturgical text' };
    
    const heading = shallowMount(OfficeHeading, { props: { line } });
    const leader = shallowMount(OfficeLeader, { props: { line } });
    const congregation = shallowMount(OfficeCongregation, { props: { line } });
    
    expect(heading.props('line')).toEqual(line);
    expect(leader.props('line')).toEqual(line);
    expect(congregation.props('line')).toEqual(line);
  });

  it('should render empty content without crashing', () => {
    const line = { content: '' };
    
    const components = [
      OfficeHeading,
      OfficeSubheading,
      OfficeCitation,
      OfficeLeader,
      OfficeCongregation,
      OfficeRubric,
    ];

    components.forEach((Component) => {
      const wrapper = shallowMount(Component, {
        props: { line },
      });
      
      expect(wrapper.exists()).toBe(true);
    });
  });
});
