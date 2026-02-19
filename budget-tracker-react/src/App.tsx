import { useState, useEffect } from 'react';
import type { Category } from './types';
import { loadCategories, saveCategories } from './storage';
import { Dashboard } from './components/Dashboard';

export default function App() {
  const [categories, setCategories] = useState<Category[]>(() => loadCategories());

  useEffect(() => {
    saveCategories(categories);
  }, [categories]);

  return <Dashboard categories={categories} />;
}
