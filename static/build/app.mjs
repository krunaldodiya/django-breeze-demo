import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext, createApp, h } from "vue";
import { createInertiaApp } from "@inertiajs/vue3";
const _export_sfc = (sfc, props) => {
  const target = sfc.__vccOpts || sfc;
  for (const [key, val] of props) {
    target[key] = val;
  }
  return target;
};
const _sfc_main = {};
function _sfc_ssrRender(_ctx, _push, _parent, _attrs) {
  _push(`<div${ssrRenderAttrs(_attrs)}>welcome</div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("resources/js/Pages/Welcome.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const Welcome = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
const __vite_glob_0_0 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Welcome
}, Symbol.toStringTag, { value: "Module" }));
createInertiaApp({
  resolve: (name) => {
    const pages = /* @__PURE__ */ Object.assign({ "./Pages/Welcome.vue": __vite_glob_0_0 });
    return pages[`./Pages/${name}.vue`];
  },
  setup({ el, App, props, plugin }) {
    createApp({ render: () => h(App, props) }).use(plugin).mount(el);
  }
});
