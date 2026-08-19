/**
 * 本地 ESLint 规则（由 eslint-plugin-local-rules 加载）。
 * - no-unicode-icon：禁止 Unicode 字符图标（需求 4）
 * - no-hardcoded-color：禁止 JS 中向 color/bg 类属性传十六进制 / rgb / hsl（需求 7）
 */

// 常见被当作图标使用的 Unicode 符号（几何形状、杂项符号、箭头、方框绘制等）
const ICON_CHARS = /[▶◀▼▲■□●◆★☆✦✕✖✓✔♥♦♠♣☑☐☒➜➤➔⟶↳⚑⭐▸▾◂►⏵⏸⏹]/;

const COLOR_PROP = /^(color|bg|background|backgroundColor|bgColor|border|borderColor|fill|stroke|textColor)$/i;
const COLOR_VALUE = /^(#([0-9a-fA-F]{3,8})|rgba?\(|hsla?\()/;

export default {
  rules: {
    'no-unicode-icon': {
      meta: {
        type: 'problem',
        docs: { description: '禁止使用 Unicode 字符作为图标，请使用 AppIcon / lucide 图标' },
        schema: [],
      },
      create(context) {
        function check(text, node) {
          if (typeof text === 'string' && ICON_CHARS.test(text)) {
            context.report({ node, message: '禁止使用 Unicode 字符图标，请改用 AppIcon / lucide 图标' });
          }
        }
        return {
          Literal(node) { check(node.value, node); },
          TemplateElement(node) { check(node.value && node.value.raw, node); },
          VText(node) { check(node.value, node); },
        };
      },
    },

    'no-hardcoded-color': {
      meta: {
        type: 'problem',
        docs: { description: '禁止在 JS 中硬编码颜色（请改用语义令牌或 CSS 变量）' },
        schema: [],
      },
      create(context) {
        return {
          Property(node) {
            const key = node.key && (node.key.name || node.key.value);
            if (!key || !COLOR_PROP.test(key)) return;
            const v = node.value;
            if (v && v.type === 'Literal' && typeof v.value === 'string' && COLOR_VALUE.test(v.value.trim())) {
              context.report({ node: v, message: `禁止硬编码颜色 "${v.value}"，请改用语义令牌（如 var(--color-accent)）` });
            }
          },
        };
      },
    },
  },
};
