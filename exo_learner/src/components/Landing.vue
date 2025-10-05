<template>
    <div class="landing">
        <h1>{{ landingData.title }}</h1>
        <p>{{ landingData.subtitle }}</p>
    </div>
</template>

<script>
import commonsData from '../assets/data/commons.json';

export default {
    name: 'Landing',
    computed: {
        landingData() {
            return commonsData.landing;
        }
    }
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