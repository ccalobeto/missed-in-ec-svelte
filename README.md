# sv

Everything you need to build a Svelte project, powered by [`sv`](https://github.com/sveltejs/cli).

## Setup Python
Choose your python virtual environment in your VS Code placed in the botton. In my case `3.12.3('py312':conda)`

## Download CSV files
Go to [Ecuador datos abiertos](https://www.datosabiertos.gob.ec/dataset/personas-desaparecidas), download the excel files and convert them to csv files. Be careful with ',' for decimals in google sheets. Move the converted files to `static/data/input`.

## Executing scripts 
Run these scripts

To install your python libraries
```javascript
npm run python:dependencies
```

To load a csv file, clean and generate one cumulated csv file
```javascript
npm run data:generate
```

To generate a json file with all summaries for your svelte project
```javascript
npm run data:summary
```

## Creating a project

If you're seeing this, you've probably already done this step. Congrats!

```bash
# create a new project in the current directory
npx sv create

# create a new project in my-app
npx sv create my-app
```

## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://svelte.dev/docs/kit/adapters) for your target environment.
