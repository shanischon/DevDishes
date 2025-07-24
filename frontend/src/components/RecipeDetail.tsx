import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

interface Recipe {
  id: string;
  name: string;
  content: string;
  image?: string;
}

const RecipeDetail: React.FC = () => {
  const { recipeId } = useParams<{ recipeId: string }>();
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetch(`/recipes/${recipeId}`)
      .then(res => {
        if (!res.ok) throw new Error('Recipe not found');
        return res.json();
      })
      .then(data => setRecipe(data))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [recipeId]);

  if (loading) return <div className="p-8 text-center">Loading...</div>;
  if (error) return <div className="p-8 text-center text-red-600">{error}</div>;
  if (!recipe) return <div className="p-8 text-center">Recipe not found.</div>;

  return (
    <div className="max-w-2xl mx-auto p-8">
      <Link to="/" className="text-amber-600 hover:underline">&larr; Back to recipes</Link>
      <h1 className="text-3xl font-bold mt-4 mb-2">{recipe.name}</h1>
      {recipe.image && <img src={recipe.image} alt={recipe.name} className="w-full rounded-lg mb-4" />}
      <p className="mb-4 text-gray-700 whitespace-pre-line">{recipe.content}</p>
    </div>
  );
};

export default RecipeDetail; 