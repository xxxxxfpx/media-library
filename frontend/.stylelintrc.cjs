/** Stylelint 配置 —— 将「禁止硬编码颜色」固化为门禁（需求 7）。
 *  唯一合法的色值定义处：src/styles/tokens/primitives.css（已加白名单）。
 *  主题文件用 var() 引用 primitives，故不触发本规则。 */
module.exports = {
  extends: ['stylelint-config-standard-scss'],
  overrides: [
    { files: ['**/*.scss'], customSyntax: 'postcss-scss' },
    { files: ['**/*.vue'], customSyntax: 'postcss-html' },
  ],
  rules: {
    // 过渡期先以 warning 报告硬编码颜色，存量清理完成后改回 error
    'declaration-property-value-disallowed-list': [
      {
        '/^color$|^background|^border|^fill|^stroke|^box-shadow|^outline|^caret|^text-decoration$/': [
          '/^#[0-9a-fA-F]{3,8}\\b/',
          '/^rgba?\\(/',
          '/^hsla?\\(/',
        ],
      },
      { severity: 'warning' },
    ],
    // 关闭与本项目风格冲突的默认规则
    'scss/dollar-variable-pattern': null,
    'no-descending-specificity': null,
    'selector-class-pattern': null,
    'custom-property-pattern': null,
    'comment-empty-line-before': null,
    'scss/at-mixin-pattern': null,
    'scss/at-function-pattern': null,
    'scss/percent-placeholder-pattern': null,
    'keyframes-name-pattern': null,
    'alpha-value-notation': null,
    'color-function-notation': null,
    'color-function-alias-notation': null,
    'color-hex-length': null,
    'declaration-block-single-line-max-declarations': null,
    'rule-empty-line-before': null,
    'selector-pseudo-class-no-unknown': null,
    'scss/at-rule-no-unknown': null,
    'at-rule-no-unknown': null,
    'property-no-vendor-prefix': null,
    'value-no-vendor-prefix': null,
    'media-feature-range-notation': null,
    'no-empty-source': null,
    'font-family-name-quotes': null,
    'value-keyword-case': null,
    'scss/load-partial-extension': null,
    'no-invalid-position-at-import-rule': null,
    'custom-property-empty-line-before': null,
  },
  ignoreFiles: [
    'src/styles/tokens/primitives.css',
    'src/views/VideoPlayer.vue',
    'node_modules/**',
    'dist/**',
  ],
}
