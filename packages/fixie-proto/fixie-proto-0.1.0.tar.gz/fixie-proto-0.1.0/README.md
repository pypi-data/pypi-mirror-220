# fixie-proto
Repository containing protos. The intention is for this to define our public-facing APIs. Tooling in this repository should then make it easy to use the *already compiled* protos in various languages.

For languages supported by the Buf Schema Registry, instructions for adding these protos like a normal dependency can be found [here](https://buf.build/fixie-ai/fixie/assets/main).  For example, to add a TypeScript dependency using yarn:

```
yarn config set npmScopes.buf.npmRegistryServer https://buf.build/gen/npm/v1/
yarn add @buf/fixie-ai_fixie.bufbuild_connect-es@latest
```

We also support additional languages (albeit with fewer options) directly. In particular, Python is available via pip: [PyPI]().
