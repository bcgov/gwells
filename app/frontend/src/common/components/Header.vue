<template>
  <header id="header">
    <Menubar :model="windowWidth <= 640 ? navItems : []" class="flex items-center print:block be-blue">
      <template #start>
        <div class="flex items-center justify-between px-4 py-2 mx-auto">
          <a class="inline-block py-1.5 mr-4 text-xl whitespace-nowrap" href="https://www2.gov.bc.ca">
            <img
                class="flex max-w-full h-auto hidden sm:block"
                src="@/common/assets/images/17_gov3_bc_logo.svg"
                width="152" height="55"
                alt="B.C. Government Logo">
            <img
                class="flex max-w-full h-auto hidden sm:block nav-logo-print"
                src="@/common/assets/images/17_gov3_bc_logo_transparent.svg"
                width="152" height="55"
                alt="B.C. Government Logo">
            <img
                class="flex max-w-full h-auto sm:hidden"
                src="@/common/assets/images/01_gov3_bc_symbol.svg"
                width="61"
                height="43"
                alt="B.C. Government Logo">
          </a>
          <div class="flex bc-nav-title hidden md:block">Groundwater Wells and Aquifers{{getEnvironmentMessage}}</div>
        </div>
      </template>
      <!-- Log in details and button -->
      <template #end>
        <keycloak-auth class="flex hidden sm:block print:hidden" v-if="auth !== 'hide'" id="keycloak-auth"/>
      </template>
      <template #item="{ item, label }">
          <router-link v-if="item" :to="item.route">
            {{ label }}
          </router-link>
      </template>
    </Menubar>
    <Menubar v-if="windowWidth > 640" class="bc-nav-links [&>ul>li+li]:border-l [&>ul>li]:border-white" :model="navItems">
      <template #item="{ item, label }">
        <router-link v-if="item" :to="item.route" class="text-white px-3 hover:underline decoration-white">
          {{ label }}
        </router-link>
      </template>
    </Menubar>
  </header>
</template>

<script>
import { useCommonStore } from '@/stores/common'
import Auth from '@/common/components/Auth.vue'
export default {
  components: {
    'keycloak-auth': Auth
  },
  props: ['auth'],
  data () {
    return {
      windowWidth: window.innerWidth
    }
  },
  computed: {
    commonStore () { return useCommonStore() },
    hasConfig () {
      return Boolean(this.commonStore.config)
    },
    getEnvironmentMessage () {
      /**
       * return a message based on the current url location,
       * if gwells-staging or testapps.nrs.gov.bc.ca in url then return ' - STAGING' otherwise ''
       */
      return (window.location.href.indexOf('gwells-staging') > -1 ||
        window.location.href.indexOf('testapps.nrs.gov.bc.ca') > -1) ? ' - STAGING' : ''
    },
    show () {
      const adminMeta = document.head.querySelector('meta[name="show.admin"]')
      let bulk = false
      if (this.commonStore.userRoles.bulk) {
        bulk = Object.values(this.commonStore.userRoles.bulk).some(x => x)
      }
      return {
        dataEntry: this.hasConfig && this.commonStore.userRoles.submissions.edit === true,
        admin: adminMeta ? adminMeta.content === 'true' : false,
        aquifers: this.hasConfig && this.commonStore.config.enable_aquifers_search === true,
        surveys: this.hasConfig && this.commonStore.userRoles.surveys.edit === true,
        qaqc: this.hasConfig && this.commonStore.userRoles.submissions.edit === true,
        bulk
      }
    },
    navItems () {
      return [
        { label: 'Well Search', route: { name: 'wells-home' }, visible: true },
        { label: 'Aquifer Search', route: { name: 'aquifers-home' }, visible: this.show.aquifers },
        { label: 'Registry Search', route: { name: 'SearchHome'}, visible: true },
        { label: 'Submit Report', route: { name: 'SubmissionsHome' }, visible: this.show.dataEntry },
        { label: 'Bulk Upload', route: { name: 'bulk-home' }, visible: this.show.bulk },
        { label: 'QA/QC Dashboard', route: { name: 'qaqc' }, visible: this.show.qaqc },
        { label: 'Admin', route: { name: 'Surveys' }, visible: this.show.surveys },
        { label: 'Groundwater Information', route: { name: 'groundwater-information' }, visible: true },
      ]
    }
  },
  mounted() {
    window.addEventListener('resize', () => {
      this.windowWidth = window.innerWidth
    })
  }
}
</script>

<style lang="scss">

.navbar {
  margin-bottom: 0px;
}
.nav-item {
  font-size: 13px;
}
.bc-nav-title {
  font-size: 2em;
  color: #fff!important;
  margin-bottom: -10px;
}
.bc-nav-links {
  background: #39598A !important;
  border-top: #F9B81B solid 3px !important;
  border-left: 0px !important;
  border-right: 0px !important;
  border-bottom: 0px !important;
  border-radius: 0px !important;
  padding-top: 0px;
  padding-bottom: 0px;
  -webkit-box-shadow: 0px 3px 3px 1px rgba(51, 51, 51, 0.5);
  -moz-box-shadow: 0px 3px 3px 1px rgba(51, 51, 51, 0.5);
  box-shadow: 0px 3px 3px 1px rgba(51, 51, 51, 0.5);
}
// override primevue highlight on hover
.bc-nav-links * {
  background-color: transparent !important;
}
.lvl2-link a {
  padding-top:0;
  padding-bottom:0;
}
.nav-logo-print {
  height: 0px !important;
}
@media print {
  header nav {
    background-color: rgba(0,0,0,0) !important;
    border-bottom: none !important;
  }
  .bc-nav-title {
    color: #000 !important;
  }
  .nav-logo-print {
    height: 55px !important;
  }
  .nav-logo {
    height: 0px !important;
  }
}
.be-blue {
  background: #003366 !important;
  border: none !important;
  border-radius: 0px !important;
}
</style>
