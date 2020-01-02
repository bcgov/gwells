/*
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/
<template>
  <div class="map-loading-spinner" v-if="loading">
    <div class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></div>
    <strong class="pl-1">Loading...</strong>
  </div>
</template>

<style>
.map-loading-spinner {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  background-color: rgba(255, 255, 255, 0.6);
  pointer-events: none;
}
</style>

<script>
export default {
  props: ['loading']
}
</script>
