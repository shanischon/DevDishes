import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Hero from './components/Hero';
import FeaturedRecipes from './components/FeaturedDishes';
import IngredientSearch from './components/IngredientSearch';
import Newsletter from './components/Newsletter';
import Footer from './components/Footer';
import Login from './components/Login';
import RecipeDetail from './components/RecipeDetail';

function Home() {
  return (
    <>
      <Header />
      <Hero />
      <FeaturedRecipes />
      <div id="ingredient-search">
        <IngredientSearch />
      </div>
      <Newsletter />
      <Footer />
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/recipes/:recipeId" element={<RecipeDetail />} />
        <Route path="/*" element={<Home />} />
      </Routes>
    </BrowserRouter>
  );
}

function LoginPage() {
  // Optionally, you can add redirect logic if already logged in
  return <Login asPage={true} />;
}

export default App;