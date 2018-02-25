<template>
    <div id="header" role="banner">
        <div id="header-main" class="navbar navbar-default navbar-fixed-top">
            <div class="container">
                <div id="header-main-row" class="row">
                    <!-- GOV TITLE -->
                    <div class="col-sm-3 col-md-2 col-lg-2 header-main-left">
                        <div id="logo">
                            <a href="http://gov.bc.ca"><img src="../../assets/images/gov3_bc_logo.png" alt="Province of British Columbia" title="Province of British Columbia logo" /></a>
                        </div>
                        <div id="access">
                            <ul>
                                <li aria-label="Keyboard Tab Skip">
                                    <a accesskey="0" href="#main-content-anchor" aria-label="Skip to main content">Skip to main content</a>
                                </li>
                                <li aria-label="Keyboard Tab Skip">
                                    <a accesskey="0" href="#navigation-anchor" aria-label="Skip to navigation">Skip to navigation</a>
                                </li>
                                <li aria-label="Keyboard Tab Skip">
                                    <a accesskey="0" href="http://gov.bc.ca/webaccessibility/" aria-label="Accessibility Statement">Accessibility Statement</a>
                                </li>
                            </ul>
                        </div>
                        <button type="button" class="navbar-toggle gov-button-custom collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="true" aria-label="Burger Navigation">
                            <img src="images/menu-open-mobile.png" />
                        </button>
                    </div>
                    <div class="col-sm-8 col-md-8 col-lg-6 hidden-xs">
                        <div class="bcgov-title">
                            <h1>Groundwater Wells and Aquifers</h1>
                        </div>
                    </div>
                    <!-- /GOV & ENV TITLE -->

                    <!-- COLLAPSING NAVBAR -->
                    <div id="navbar" class="collapse navbar-collapse" role="navigation">
                        <a id="navigation-anchor"></a>
                        <ul class="nav navbar-nav">
                            <li><a href="#">Search</a></li>
                            <li><a href="#">Groundwater Information</a></li>
                            <li><a href="#">Registry</a></li>
                            <li><a href="#">Submit Report</a></li>
                        </ul>
                    </div>
                    <!-- /COLLAPSING NAVBAR -->
                </div>
            </div>
            <div class="navigationRibbon">
                <div class="level2Navigation">
                    <div class="container">
                        <a href="#">Search</a>
                        <a href="#">Groundwater Information</a>
                        <a href="#">Registry</a>
                        <a href="#">Submit Report</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {

}
</script>

<style>

</style>
