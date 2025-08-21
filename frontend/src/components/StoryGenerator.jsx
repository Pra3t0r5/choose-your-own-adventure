import ThemeInput from "./ThemeInput";
import LoadingStatus from "./LoadingStatus";
import { API_BASE_URL } from "../constants";
import axios from "axios";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const StoryGenerator = () => {
  const navigate = useNavigate();
  const [theme, setTheme] = useState("");
  const [jobId, setJobId] = useState(null);
  const [jobStatus, setJobStatus] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateStory = async (theme) => {
    setLoading(true);
    setError(null);
    setTheme(theme);

    try {
      const response = await axios.post(`${API_BASE_URL}/stories/create`, {
        theme,
      });
      const { job_id, status } = response.data;
      setJobId(job_id);
      setJobStatus(status);

      pollJobStatus(job_id);
    } catch (e) {
      setError(`Failed to generate story: ${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  const fetchStory = (id) => {
    try {
      setLoading(true);
      setJobStatus("completed");
      navigate(`/story/${id}`);
    } catch (err) {
      setError(`Failed to load story: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const pollJobStatus = async (id) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/jobs/${id}`);
      const { status, story_id, error: jobError } = response.data;
      setJobStatus(status);

      if (status === "completed") {
        fetchStory(story_id);
      } else if (status === "failed" || jobError) {
        setError(jobError || "Failed to generate story");
      }
    } catch (e) {
      if (e.response?.status !== 404) {
        setError(`Failed to check story status: ${e.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setJobId(null);
    setJobStatus(null);
    setTheme("");
    setError(null);
    setLoading(null);
  };

  useEffect(() => {
    let pollInterval;

    if (jobId && jobStatus === "processing") {
      pollInterval = setInterval(() => {
        pollJobStatus(jobId);
      }, 5000);
    }

    return () => {
      if (pollInterval) {
        clearInterval(pollInterval);
      }
    };
  }, [jobId, jobStatus]);

  return (
    <div className="story-generator">
      {error && (
        <div className="error-message">
          <p>{error}</p>
          <button onClick={reset}>Try Again</button>
        </div>
      )}

      {!jobId && !error && !loading && <ThemeInput onSubmit={generateStory} />}

      {loading && <LoadingStatus theme={theme} />}
    </div>
  );
};

export default StoryGenerator;
