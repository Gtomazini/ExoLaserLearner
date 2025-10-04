<template>
    <div class="landing">
        <h1>Bem-vindo ao Exo Learner</h1>
        <p>Explore o universo com nossa plataforma interativa!</p>
    </div>
</template>

<script>
export default {
    name: 'Landing',
};
</script>

<style scoped>
.landing {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 80vh;
}

.landing h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.landing p {
    font-size: 1.2rem;
    color: #555;
}
</style>