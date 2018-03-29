<template>
  <div>
    <router-view/>
  </div>
</template>

<script>
// import Header from '@/common/components/Header'
// import Footer from '@/common/components/Footer'
export default {
  name: 'App',
  components: {
    // 'gwells-header': Header,
    // 'gwells-footer': Footer
  }
}
</script>

<style>
@import url('https://unpkg.com/bootstrap@3.3.7/dist/css/bootstrap.min.css');
@import url('https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css');
@import '../../../gwells/static/gwells/css/ie10-viewport-bug-workaround.css';
@import '../../../gwells/static/gwells/css/main.css';
@import '../../../gwells/static/gwells/css/custom-main.css';

.row.no-pad {
  margin-right:0;
  margin-left:0;
}
.row.no-pad > [class*='col-'] {
  padding-right:0;
  padding-left:0;
}
.panel.no-pad {
  margin-right:0;
  margin-left:0;
  padding-right:0;
  padding-left:0;
  margin-top:0;
  padding-top:0;
}
.panel.no-pad > .panel-body {
  margin-right:0;
  margin-left:0;
  padding-right:0;
  padding-left:0;
  margin-top:0;
  padding-top:0;
}
.container-fluid.no-pad {
  margin-right:0;
  margin-left:0;
  padding-right:0;
  padding-left:0;
}
.registry-panel-title {
  margin-left: 10px;
  margin-top: 0px;
  padding-top:0px;
}
.form-spacing {
  margin-bottom: 15px;
}
.registry-disabled-item {
  color: #808080;
  cursor: auto!important;
}
.register-legal {
  margin-top: 25px;
}
.btn {
    display: inline-block;
    padding: 7px 12px 5px 12px;
    margin-bottom: 0;
    font-size: 14px;
    font-weight: normal;
    line-height: 1.42857143;
    text-align: center;
    white-space: nowrap;
    vertical-align: middle;
    -ms-touch-action: manipulation;
    touch-action: manipulation;
    cursor: pointer;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    background-image: none;
    border: 1px solid;
    border-radius: 0px;
}
.btn-primary {
    color: #fff;
    background-color: #38598a;
    border-color: #003366;
}

    .btn-primary:focus,
    .btn-primary.focus {
        color: #fff;
        background-color: #003366;
        border-color: #003366;
    }

    .btn-primary:hover {
        color: #fff;
        background-color: #003366;
        border-color: #003366;
    }

    .btn-primary:active,
    .btn-primary.active,
    .open > .dropdown-toggle.btn-primary {
        color: #fff;
        background-color: #003366;
        border-color: #003366;
        background-image: none;
    }

        .btn-primary:active:hover,
        .btn-primary.active:hover,
        .open > .dropdown-toggle.btn-primary:hover,
        .btn-primary:active:focus,
        .btn-primary.active:focus,
        .open > .dropdown-toggle.btn-primary:focus,
        .btn-primary:active.focus,
        .btn-primary.active.focus,
        .open > .dropdown-toggle.btn-primary.focus {
            color: #fff;
            background-color: #204d74;
            border-color: #003366;
        }

    .btn-primary.disabled,
    .btn-primary.disabled:hover,
    .btn-primary[disabled]:hover,
    fieldset[disabled] .btn-primary:hover,
    .btn-primary.disabled:focus,
    .btn-primary[disabled]:focus,
    fieldset[disabled] .btn-primary:focus,
    .btn-primary.disabled.focus,
    .btn-primary[disabled].focus,
    fieldset[disabled] .btn-primary.focus {
        background-color: #337ab7;
        border-color: #2e6da4;
    }

    .btn-primary .badge {
        color: #337ab7;
        background-color: #fff;
}
.btn-default {
    color: #333;
    background-color: #d1d1d1;
    border-color: #afafaf;
}

    .btn-default:focus,
    .btn-default.focus {
        color: #333;
        background-color: #afafaf;
        border-color: #88929a;
    }

    .btn-default:hover {
        color: #333;
        background-color: #afafaf;
        border-color: #88929a;
    }

    .btn-default:active,
    .btn-default.active,
    .open > .dropdown-toggle.btn-default {
        color: #333;
        background-color: #afafaf;
        border-color: #88929a;
        background-image: none;
    }

        .btn-default:active:hover,
        .btn-default.active:hover,
        .open > .dropdown-toggle.btn-default:hover,
        .btn-default:active:focus,
        .btn-default.active:focus,
        .open > .dropdown-toggle.btn-default:focus,
        .btn-default:active.focus,
        .btn-default.active.focus,
        .open > .dropdown-toggle.btn-default.focus {
            color: #333;
            background-color: #afafaf;
            border-color: #88929a;
        }

    .btn-default.disabled,
    .btn-default.disabled:hover,
    .btn-default[disabled]:hover,
    fieldset[disabled] .btn-default:hover,
    .btn-default.disabled:focus,
    .btn-default[disabled]:focus,
    fieldset[disabled] .btn-default:focus,
    .btn-default.disabled.focus,
    .btn-default[disabled].focus,
    fieldset[disabled] .btn-default.focus {
        background-color: #fff;
        border-color: #ccc;
    }

    .btn-default .badge {
        color: #fff;
        background-color: #333;
}
</style>
