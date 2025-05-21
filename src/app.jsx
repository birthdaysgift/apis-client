import Router from 'preact-router';

import HomePage from './pages/home/homePage';
import ComponentsPage from './pages/components/componentsPage';
import ColorsPage from './pages/colors/colorsPage';
import FontsPage from './pages/fonts/fontsPage';
import LayoutsPage from './pages/layouts/layoutsPage';


export function App() {
  return (
    <div>
      <Router>
        <HomePage path="/" />
        <ColorsPage path="/colors" />
        <ComponentsPage path="/components" />
        <FontsPage path="/fonts" />
        <LayoutsPage path="/layouts" />
      </Router>
    </div>
  )
}
