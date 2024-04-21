import "./App.css";
import axios from "axios";

function App() {
  const onClickHandler = async () => {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:5000/upload", formData);

      console.log(response);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className="App">
      <input type="file" name="image" id="fileInput" />
      <button onClick={onClickHandler}>Submit</button>
    </div>
  );
}

export default App;
