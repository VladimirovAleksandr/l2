<template>
  <div v-frag>
    <div class="top-buttons" :class="!confirmed && 'top-buttons-full'">
      <template v-if="loaded">
        <template v-if="!confirmed">
          <button class="btn btn-blue-nb btn-ell" @click="openRefSettings()">
            Настройка референсов
          </button>
          <button class="btn btn-blue-nb btn-ell" @click="save()">
            Сохранить
          </button>
          <button class="btn btn-blue-nb btn-ell" :disabled="!saved" @click="confirm()">
            Подтвердить
          </button>
          <button class="btn btn-blue-nb btn-ell" @click="saveAndConfirm()">
            Сохранить и подтвердить
          </button>
        </template>
        <template v-else>
          <button class="btn btn-blue-nb btn-right" :disabled="!allow_reset_confirm" @click="resetConfirm()">
            Сброс подтверждения
          </button>
        </template>
      </template>
    </div>
    <div class="root" ref="root" v-show="pk">
      <table class="table table-bordered table-sm-pd" v-if="pk">
        <colgroup>
          <col style="width: 29%" />
          <col style="width: 31px" />
          <col />
          <col v-if="!noRefs" style="width: 21%" />
          <col v-if="!noRefs" style="width: 21%" />
        </colgroup>
        <thead>
          <tr>
            <td colspan="5">
              <strong>
                {{ research.title }}
              </strong>
            </td>
          </tr>
          <tr class="table-header">
            <th>Фракция</th>
            <td class="x-cell">
              <button
                class="btn btn-sm btn-cell"
                @click.prevent="clearAll"
                v-if="!confirmed"
                title="Очистить все значения"
                v-tippy
              >
                <i class="fa fa-times"></i>
              </button>
            </td>
            <th>Значение</th>
            <th v-if="!noRefs">Нормы М</th>
            <th v-if="!noRefs">Нормы Ж</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(r, i) in result" :key="r.fraction.pk">
            <td>
              <label class="fraction-title" :for="`fraction-${r.fraction.pk}`">{{ r.fraction.title }}</label>
            </td>
            <BloodTypeField v-if="research.template === 2 && i === 0" :readonly="confirmed || !loaded" :r="r" />
            <template v-else>
              <td class="x-cell">
                <button
                  class="btn btn-sm btn-cell"
                  @click.prevent="clear(r)"
                  v-if="!confirmed"
                  :title="`Очистить ${r.fraction.title}`"
                  v-tippy
                  tabindex="-1"
                >
                  <i class="fa fa-times"></i>
                </button>
              </td>
              <TextInputField
                :readonly="confirmed || !loaded"
                :move-focus-next="moveFocusNext"
                :r="r"
                :allDirPks="allDirPks"
                :dirData="dirData"
              />
            </template>
            <Ref :data="r.ref.m" v-if="!noRefs" />
            <Ref :data="r.ref.f" v-if="!noRefs" />
          </tr>
          <tr v-if="research.can_comment">
            <td><label class="fraction-title" for="result_comment">Комментарий</label></td>
            <td colspan="4">
              <textarea
                class="noresize form-control result-field"
                :readonly="confirmed || !loaded"
                v-autosize="comment"
                v-model="comment"
                id="result_comment"
              ></textarea>
            </td>
          </tr>
          <template v-if="research.co_executor_mode > 0 && laborants.length > 0">
            <tr>
              <td colspan="5">
                <hr />
              </td>
            </tr>
            <tr>
              <td>
                <label for="laborant">Лаборант</label>
              </td>
              <td colspan="4">
                <treeselect
                  :multiple="false"
                  :disable-branch-nodes="true"
                  :options="laborants"
                  placeholder="Лаборант не выбран"
                  v-model="co_executor"
                  :append-to-body="true"
                  :clearable="false"
                  id="laborant"
                  :disabled="confirmed"
                />
              </td>
            </tr>
            <tr>
              <td>
                <label for="co_executor2">{{ research.co_executor_title }}</label>
              </td>
              <td colspan="4">
                <treeselect
                  :multiple="false"
                  :disable-branch-nodes="true"
                  :options="laborants"
                  placeholder="Соисполнитель не выбран"
                  v-model="co_executor2"
                  :append-to-body="true"
                  :clearable="false"
                  id="co_executor2"
                  :disabled="confirmed"
                />
              </td>
            </tr>
          </template>
          <tr v-else-if="legalAuthenticator">
            <td colspan="5">
              <hr />
            </td>
          </tr>
          <tr v-if="legalAuthenticator">
            <td>
              <label for="laborant">Подпись от организации</label>
            </td>
            <td colspan="4">
              <treeselect
                :multiple="false"
                :disable-branch-nodes="true"
                :options="legalAuthenticators"
                placeholder="Не выбрано"
                v-model="legal_authenticator"
                :append-to-body="true"
                :clearable="false"
                id="legal_authenticator"
                :disabled="confirmed"
              />
            </td>
          </tr>
        </tbody>
      </table>
      <table class="table table-bordered table-condensed" v-if="pk && execParams.length > 0">
        <colgroup>
          <col width="208" />
          <col />
        </colgroup>
        <tbody>
          <tr v-for="r in execParams" :key="`${r[0]}_${r[1]}`">
            <th>{{ r[0] }}</th>
            <td>{{ r[1] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="bottom-buttons" :class="!confirmed && 'bottom-buttons-full'">
      <template v-if="loaded">
        <template v-if="!confirmed">
          <button class="btn btn-blue-nb btn-ell" @click="openRefSettings()">
            Настройка референсов
          </button>
          <button class="btn btn-blue-nb btn-ell" @click="save()">
            Сохранить
          </button>
          <button class="btn btn-blue-nb btn-ell" :disabled="!saved" @click="confirm()">
            Подтвердить
          </button>
          <button class="btn btn-blue-nb btn-ell" @click="saveAndConfirm()">
            Сохранить и подтвердить
          </button>
        </template>
        <template v-else>
          <button class="btn btn-blue-nb btn-right" :disabled="!allow_reset_confirm" @click="resetConfirm()">
            Сброс подтверждения
          </button>
        </template>
      </template>
    </div>
    <RefSettings v-if="showRefSettings" :close="hideRefSettings" :result="result" />
  </div>
</template>
<script lang="ts">
import Treeselect from '@riophae/vue-treeselect';
import '@riophae/vue-treeselect/dist/vue-treeselect.css';

import * as actions from '@/store/action-types';
import Ref from '@/pages/LaboratoryResults/Ref.vue';
import TextInputField from '@/pages/LaboratoryResults/TextInputField.vue';
import BloodTypeField from '@/pages/LaboratoryResults/BloodTypeField.vue';
import RefSettings from '@/pages/LaboratoryResults/RefSettings.vue';

export default {
  name: 'ResultsForm',
  components: {
    RefSettings,
    TextInputField,
    BloodTypeField,
    Ref,
    Treeselect,
  },
  mounted() {
    this.$root.$on('laboratory:results:open-form', (pk, allDirPks, dirData) => {
      this.loadForm(pk);
      this.allDirPks = allDirPks;
      this.dirData = dirData;
    });
    this.$root.$on('laboratory:reload-form', () => this.reloadForm());
  },
  data() {
    return {
      loaded: false,
      confirmed: false,
      saved: false,
      allow_reset_confirm: false,
      showRefSettings: false,
      pk: null,
      research: {},
      execData: {},
      comment: '',
      result: [],
      allDirPks: [],
      dirData: {},
      laborants: [],
      co_executor: -1,
      co_executor2: -1,
      legalAuthenticators: [],
      legal_authenticator: -1,
    };
  },
  computed: {
    noRefs() {
      return this.research.no_units_and_ref || this.research.template === 2;
    },
    execParams() {
      const r = [];
      if (this.execData.timeSave) {
        r.push(['Время сохранения', this.execData.timeSave]);
      }
      if (this.execData.docSave) {
        r.push(['Сохранил', this.execData.docSave]);
      }
      if (this.execData.timeConfirm) {
        r.push(['Время подтверждения', this.execData.timeConfirm]);
      }
      if (this.execData.docConfirmation) {
        r.push(['Подтвердил', this.execData.docConfirmation]);
      }
      if (this.execData.app) {
        r.push(['Анализатор', this.execData.app]);
      }
      return r;
    },
    legalAuthenticator() {
      return !!this.$store.getters.modules.legal_authenticator;
    },
  },
  methods: {
    async loadForm(pk) {
      this.loaded = false;
      if (pk === -1) {
        this.pk = null;
        this.research = {};
        this.execData = {};
        this.comment = '';
        this.result = [];
        this.confirmed = false;
        this.saved = false;
        this.allow_reset_confirm = false;
        return;
      }
      await this.$store.dispatch(actions.INC_LOADING);
      const { data } = await this.$api('laboratory/form', { pk });
      this.pk = data.pk;
      this.research = data.research;
      this.execData = data.execData;
      this.comment = data.comment;
      this.result = data.result;
      this.confirmed = data.confirmed;
      this.saved = data.saved;
      this.laborants = data.laborants;
      this.co_executor = data.co_executor;
      this.co_executor2 = data.co_executor2;
      this.allow_reset_confirm = data.allow_reset_confirm;
      this.legalAuthenticators = data.legalAuthenticators;
      this.legal_authenticator = data.legal_authenticator;
      this.loaded = true;
      window.$(this.$refs.root).scrollTop(0);
      if (!data.confirmed) {
        setTimeout(() => {
          const $rf = window.$('.result-field:not([readonly]):not([disabled])');
          if ($rf.length) {
            const idx = data.result.findIndex(r => !r.value);
            if (idx !== -1) {
              $rf.eq(idx).focus();
            }
          }
        }, 0);
      }
      await this.$store.dispatch(actions.DEC_LOADING);
    },
    async clearAll() {
      try {
        await this.$dialog.confirm('Вы действительно очистить все значения?');
      } catch (_) {
        return;
      }
      for (const i of this.result) {
        i.value = '';
      }
    },
    clear(r) {
      // eslint-disable-next-line no-param-reassign
      r.value = '';
      this.$root.$emit('msg', 'ok', `Очищено: ${r.fraction.title}`, 2000);
      setTimeout(() => window.$(`#fraction-${r.fraction.pk}`).focus(), 50);
    },
    async save(withoutReloading = false) {
      await this.$store.dispatch(actions.INC_LOADING);
      const { ok, message } = await this.$api('laboratory/save', this, [
        'pk',
        'result',
        'comment',
        'co_executor',
        'co_executor2',
        'legal_authenticator',
      ]);
      if (!ok) {
        this.$root.$emit('msg', 'error', message);
      } else {
        this.$root.$emit('msg', 'ok', 'Сохранено');
      }
      if (!withoutReloading) {
        this.$root.$emit('laboratory:reload-direction:with-open-first');
      }
      await this.$store.dispatch(actions.DEC_LOADING);
      return ok;
    },
    async confirm() {
      await this.$store.dispatch(actions.INC_LOADING);
      const { ok, message } = await this.$api('laboratory/confirm', this, 'pk');
      if (!ok) {
        this.$root.$emit('msg', 'error', message);
      } else {
        this.$root.$emit('msg', 'ok', 'Подтверждено');
      }
      this.$root.$emit('laboratory:reload-direction:with-open-first');
      await this.$store.dispatch(actions.DEC_LOADING);
      return ok;
    },
    async saveAndConfirm() {
      const saveResult = await this.save(true);
      if (!saveResult) {
        return;
      }

      await this.confirm();
    },
    async resetConfirm() {
      try {
        await this.$dialog.confirm('Подтвердите сброс');
      } catch (_) {
        return;
      }
      await this.$store.dispatch(actions.INC_LOADING);
      const { ok, message } = await this.$api('laboratory/reset-confirm', this, 'pk');
      if (!ok) {
        this.$root.$emit('msg', 'error', message);
      } else {
        this.$root.$emit('msg', 'ok', 'Подтверждение сброшено');
      }
      this.reloadForm();
      await this.$store.dispatch(actions.DEC_LOADING);
    },
    reloadForm() {
      this.$root.$emit('laboratory:reload-direction:with-open-pk', this.pk);
    },
    moveFocusNext(e) {
      const $rf = window.$('.result-field:not([readonly]):not([disabled])');
      const index = $rf.index(e.target) + 1;
      if ($rf.eq(index).length) {
        $rf.eq(index).focus();
      } else {
        this.save();
      }
    },
    openRefSettings() {
      this.showRefSettings = true;
    },
    hideRefSettings() {
      this.showRefSettings = false;
    },
  },
};
</script>

<style scoped lang="scss">
.root {
  position: absolute;
  top: 34px !important;
  right: 0;
  left: 0;
  bottom: 34px !important;
  overflow-x: visible;
  overflow-y: auto;
}

.fraction-title {
  font-weight: normal;
  font-size: 14px;
  display: block;
  min-height: 100%;
  height: 100%;
  margin: 0;
  cursor: pointer !important;
}

.header-button {
  width: 100%;
  max-width: 150px;
  float: right;
}

.table-header {
  th,
  td {
    position: sticky;
    top: -1px;
    background-color: white;
    z-index: 101;
    box-shadow: 2px 0 2px rgba(0, 0, 0, 0.1);
  }

  th {
    padding: 2px 2px 2px 8px;
  }

  td {
    strong {
      padding: 2px 2px 2px 8px;
    }
  }
}
</style>
