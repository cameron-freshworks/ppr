// Libraries
import Vue from 'vue'
import Vuetify from 'vuetify'
import { getVuexStore } from '@/store'
import CompositionApi from '@vue/composition-api'
import { mount, createLocalVue, Wrapper } from '@vue/test-utils'

// Components
import { SearchHistory } from '@/components/tables'

// Other
import { searchTableHeaders } from '@/resources'
import { SearchHistoryResponseIF } from '@/interfaces'
import { APISearchTypes, UISearchTypes } from '@/enums'
import { mockedSearchHistory } from './test-data'

// Vue.use(CompositionApi)
Vue.use(Vuetify)

const vuetify = new Vuetify({})
const store = getVuexStore()

// Input field selectors / buttons
const historyTable: string = '#search-history-table'
const noResultsInfo: string = '#no-history-info'

/**
 * Creates and mounts a component, so that it can be tested.
 *
 * @returns a Wrapper<SearchedResult> object with the given parameters.
 */
function createComponent (): Wrapper<any> {
  const localVue = createLocalVue()
  localVue.use(CompositionApi)
  localVue.use(Vuetify)
  document.body.setAttribute('data-app', 'true')
  return mount(SearchHistory, {
    localVue,
    store,
    vuetify
  })
}
describe('Test result table with no results', () => {
  let wrapper: Wrapper<any>

  beforeEach(async () => {
    await store.dispatch('setSearchHistory', [])
    wrapper = createComponent()
  })
  afterEach(() => {
    wrapper.destroy()
  })

  it('renders and displays correct elements for no results', async () => {
    expect(wrapper.findComponent(SearchHistory).exists()).toBe(true)
    expect(wrapper.vm.historyLength).toBe(0)
    expect(wrapper.find(historyTable).exists()).toBe(false)
    const noResultsDisplay = wrapper.findAll(noResultsInfo)
    expect(noResultsDisplay.length).toBe(1)
    expect(noResultsDisplay.at(0).text()).toContain('Your search history will display here')
  })
})

describe('Test result table with results', () => {
  let wrapper: Wrapper<any>

  beforeEach(async () => {
    await store.dispatch('setSearchHistory', mockedSearchHistory.searches)
    wrapper = createComponent()
  })
  afterEach(() => {
    wrapper.destroy()
  })

  it('renders and displays correct elements with results', async () => {
    expect(wrapper.findComponent(SearchHistory).exists()).toBe(true)
    expect(wrapper.vm.historyLength).toBe(mockedSearchHistory.searches.length)
    expect(wrapper.vm.searchHistory).toStrictEqual(mockedSearchHistory.searches)
    expect(wrapper.find(noResultsInfo).exists()).toBe(false)
    const historyTableDisplay = wrapper.findAll(historyTable)
    expect(historyTableDisplay.length).toBe(1)
    const rows = wrapper.findAll('tr')
    // includes header so add 1
    expect(rows.length).toBe(mockedSearchHistory.searches.length + 1)
    for (let i; i < mockedSearchHistory.searches; i++) {
      const searchQuery = mockedSearchHistory.searches[i].searchQuery
      const searchDate = mockedSearchHistory.searches[i].searchDateTime
      const totalResultsSize = mockedSearchHistory.searches[i].totalResultsSize
      const exactResultsSize = mockedSearchHistory.searches[i].exactResultsSize
      const selectedResultsSize = mockedSearchHistory.searches[i].selectedResultsSize
      expect(rows.at(i + 1).text()).toContain(wrapper.vm.displaySearchValue(searchQuery))
      expect(rows.at(i + 1).text()).toContain(wrapper.vm.displayType(searchQuery.type))
      expect(rows.at(i + 1).text()).toContain(searchQuery.clientReferenceId)
      expect(rows.at(i + 1).text()).toContain(wrapper.vm.displayDate(searchDate))
      expect(rows.at(i + 1).text()).toContain(totalResultsSize)
      expect(rows.at(i + 1).text()).toContain(exactResultsSize)
      expect(rows.at(i + 1).text()).toContain(selectedResultsSize)
    }
  })
})
