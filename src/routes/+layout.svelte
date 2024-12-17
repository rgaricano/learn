<script lang="ts">
	import '../app.css';
	let { children } = $props();
</script>

<svelte:head>
	<title>Learn</title>
</svelte:head>

{@render children()}
