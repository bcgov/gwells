<template>
  <fieldset>
    <div class="grid grid-cols-12">
      <div class="col-span-12 lg:col-span-6">
        <legend :id="id">{{ title }}</legend>
        <p v-if="subtitle">{{ subtitle }}</p>
      </div>
      <div v-if="!hideSave" class="col-span-12 lg:col-span-6">
        <div class="ml-auto">
          <Button v-if="isStaffEdit" label="Save" class="ml-2" @click="$emit('save')" :disabled="saveDisabled"/>
          <back-to-top-link v-if="isStaffEdit"/>
        </div>
      </div>
    </div>
    <slot />
  </fieldset>
</template>


<script>

export default {
  props: {
    title: {
      required: true,
      type: String
    },
    subtitle: String,
    hideSave: Boolean,
    id: {
      type: String,
      isInput: false
    },
    isStaffEdit: {
      type: Boolean,
      isInput: false
    },
    saveDisabled: {
      type: Boolean,
      isInput: false
    }
  },
  emits: ['save'],
  computed: {
  },
  methods: {
  },
  watch: {
  },
  data () {
    return {
    }
  }
}
</script>

<style>

</style>
