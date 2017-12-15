import departments_directory from '../../api/departments-directory'
import * as types from '../mutation-types'
import _ from 'lodash'

const state = {
  all: [],
  old_all: [],
  can_edit: false,
  types: []
}

const getters = {
  allDepartments: state => state.all,
  oldDepartments: state => state.old_all,
}

const actions = {
  async getAllDepartments({commit}) {
    const departments = await departments_directory.getDepartments()
    commit(types.UPDATE_DEPARTMENTS, {departments})
    commit(types.UPDATE_OLD_DEPARTMENTS, {departments})
  },
  updateDepartments: _.debounce(({commit, getters}) => {
    let diff = []
    let departments = getters.allDepartments
    for (let row of departments) {
      for (let in_row of getters.oldDepartments) {
        if (in_row.pk === row.pk) {
          if (in_row.title !== row.title) {
            diff.push(row)
          }
          break
        }
      }
    }
    if (diff.length === 0)
      return
    console.log(diff)
    commit(types.UPDATE_OLD_DEPARTMENTS, {departments})
  }, 650)
}

const mutations = {
  [types.UPDATE_DEPARTMENTS](state, {departments}) {
    state.all = departments
  },
  [types.UPDATE_OLD_DEPARTMENTS](state, {departments}) {
    state.old_all = JSON.parse(JSON.stringify(departments))
  },
}

export default {
  state,
  getters,
  actions,
  mutations,
}
