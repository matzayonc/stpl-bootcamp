import type {PrismTheme} from 'prism-react-renderer';

// Mirrors \lstset in preamble.tex: white base, red bold keywords,
// muted comments and strings, card background.
const stplPrism: PrismTheme = {
  plain: {
    color: '#FFFFFF',
    backgroundColor: '#161A1B',
  },
  styles: [
    {
      types: ['comment', 'prolog', 'doctype', 'cdata'],
      style: {color: '#8A9BA8'},
    },
    {
      types: ['string', 'char', 'attr-value', 'inserted'],
      style: {color: '#8A9BA8'},
    },
    {
      types: ['keyword', 'builtin', 'macro', 'lifetime-annotation'],
      style: {color: '#DC143C', fontWeight: 'bold'},
    },
    {
      types: ['class-name', 'type-definition', 'namespace'],
      style: {color: '#FFFFFF'},
    },
    {
      types: ['function', 'function-definition', 'attribute', 'property'],
      style: {color: '#FFFFFF'},
    },
    {
      types: ['punctuation', 'operator'],
      style: {color: '#C8D0D6'},
    },
    {
      types: ['number', 'boolean', 'constant', 'symbol'],
      style: {color: '#FFFFFF'},
    },
    {
      types: ['deleted'],
      style: {color: '#DC143C'},
    },
  ],
};

export default stplPrism;
