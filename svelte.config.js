// import adapter from '@sveltejs/adapter-auto';
import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { sveltePreprocess } from 'svelte-preprocess'; 
import { searchForWorkspaceRoot } from 'vite';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: [
		sveltePreprocess(),
		vitePreprocess()
	],

	kit: {
		adapter: adapter({
			fallback: '404.html'
		}),
		paths: {
			base: process.argv.includes('dev') ? '' : process.env.BASE_PATH
		}
	},
	server: {
		fs: {
			allow: [
				searchForWorkspaceRoot(process.cwd()),
				'/static'
			]
		}
	}
};

export default config
