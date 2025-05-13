const RecipeCard = ({ recipe }) => {
  const { title, image_url, image, source_url, ready_in_minutes, servings } = recipe;

  return (
    <div className="card">
      <img src={image_url || image || "https://via.placeholder.com/300"} alt={title} />
      <h3>{title}</h3>
      <div className="card-info">
        {ready_in_minutes && <span>⏱ {ready_in_minutes} mins</span>}
        {servings && <span>🍽 {servings} servings</span>}
      </div>
      {source_url && (
        <a href={source_url} target="_blank" rel="noopener noreferrer">View Recipe</a>
      )}
    </div>
  );
};

export default RecipeCard;
