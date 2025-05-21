## First time setup

_Go to project root directory._

```bash
# 1. Install nvm.
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

# 2. Install node.
nvm install

# 3. Activate node.
nvm use

# 4. Install dependencies.
npm clean-install
```


## Dev session setup

_Go to project root directory._

```bash
# 1. Activate node.
nvm use

# 2. Run dev server.
npm run dev
```

Other scripts from `package.json`:

- `npm run build` - build a bundle.
- `npm run preview` - serve production build.

