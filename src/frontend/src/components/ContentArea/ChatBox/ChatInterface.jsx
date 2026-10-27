import {useRef, useState, useEffect } from 'react';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

import { 
  getStoryAPI, 
  generateNewStoryPageAPI,
  generateBackgroundStory,
  evaluateLastActionAPI,
  getActionHistoryAPI,
  endStoryAPI
} from '@api/story';
import {
  SquarePen
} from 'lucide-react';
export default function StoryArea({ setActions }) {
  const [inputText, setInputText] = useState('');
  const textareaRef = useRef(null);
  const [isSending, setIsSending] = useState(false);
  
  const navigate = useNavigate();
  const location = useLocation(); 


  const [page_count, setPageCount] = useState(0);
  const initialStory = location.state?.story;

  const [story, setStory] = useState(initialStory);
  const { story_id, profile_id } = useParams();

  // Determine if the story is expired/inactive
  const isExpired = story && story.is_active !== true;

  // Load Story
  useEffect(() => {
      if (initialStory) {
          setStory(initialStory);
          setPageCount(initialStory.pages.length);
          return; 
      }

        async function loadStory() {
          try {
              const response = await getStoryAPI(story_id);
              setStory(response);
              setPageCount(response.pages.length);
          } catch (err) {
              console.error('Failed to load story:', err);
              navigate(`/`, {
                state: { toast: { type: "failed", message: "Can't load story" } }
              });
          }
      };

      if (story_id) {
          loadStory();
      }
  }, [story_id, initialStory, navigate]);

  // Load Action History
  useEffect(() => {
    const loadActions = async () => {
      try {
        const actions = await getActionHistoryAPI(story_id);
        setActions(actions);
      } catch (err) {
        console.error('Failed to load action history:', err);
      }
    };

    if (story_id) {
        loadActions();
    }
  }, [story_id, setActions]);

const handleInputChange = (e) => {
    setInputText(e.target.value);
    
    // Auto-expand logic
    const textarea = textareaRef.current;
    if (textarea) {
      // Reset height to 'auto' to recalculate shrinkage if user deletes text
      textarea.style.height = 'auto';
      // Set height to scrollHeight (the total height of the text content)
      textarea.style.height = `${textarea.scrollHeight}px`;
    }
  };

  const handleKeyDown = (e) => {
    // Send message on Enter, but allow Shift+Enter for new lines
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault(); // Prevent adding a new line
      if (!isSending && !isExpired && inputText.trim()) {
        handleSubmit(inputText);
      }
    }
  };
const handleSubmit = async (textToSubmit) => {
    setIsSending(true);  
    
    try {
      const newPage = await generateNewStoryPageAPI(
        story_id,
        textToSubmit
      );

      setStory(prevStory => {
        if (!prevStory) return prevStory;
        return {
          ...prevStory,
          pages: [...prevStory.pages, newPage]
        };
      });
      
      const newEvaluations = await evaluateLastActionAPI(story_id);

      setActions(prevActions => [
        ...(prevActions || []),
        ...newEvaluations
      ]);
      
      setPageCount(prev => prev + 1);
      

    } catch (err) {
        console.error("Failed to generate new story page:", err);
    } finally {
      setInputText(''); 
      setIsSending(false);
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };


  const handleEndStory = async () => {
    try {
      await endStoryAPI(story_id);

      navigate(`/profile/${profile_id}/me_active_profile`, {
        state: { toast: { type: "success", message: "Story ended." } }
      });

    } catch (err) {
      console.error(err);
    }
  };
  const handleRegenerateBackground = async () => {
      setIsSending(true); // Tell the UI we are loading
      const textToSubmit = inputText.trim() || "Regenerate";
      try {
        const response = await generateBackgroundStory(
          story_id,
          textToSubmit
        );
        setStory(response); 
        window.dispatchEvent(new CustomEvent("storyCreated"));
        setPageCount(1);
      } catch (err) {
        // If the API fails, this will now catch the error and log it
        console.error("Failed to regenerate background:", err);
        alert("Failed to regenerate the background, please make sure you have set goals and answers. Check the console for details.");
      } finally {
        setInputText(''); 
        setIsSending(false);
        if (textareaRef.current) {
          textareaRef.current.style.height = 'auto';
        }
    }
    };

return (
  <div className="content-area-container">

    <div className="floating-button-row">
        <button
          onClick={() => navigate(`/profile/${profile_id}/me_active_profile`)}
        >
            Check your goals!
        </button>
        <button
          onClick={() => navigate(`/profile/${profile_id}/stories/${story_id}/init`)}
        >
                    Personalize your Experience
        </button>
        {story?.is_active === true && (
          <button
            onClick={handleEndStory}
          >
            End this story
          </button>
        )}
      {story?.is_active === true && (
        <button
          onClick={handleRegenerateBackground}
          disabled={isSending}
        >
          {isSending ? "Regenerating..." : "Reset and get new task "}
        </button>
      )}


        
    </div>
      <>


        {/* Greeting for brand new stories */}
        {!story && (
          <header className="chat-header">
            <h1>Loading your task...</h1>
          </header>
        )}

        {/* Chat / Story History */}
    <div className="chat-history">
      {story && (
        <>
          <div className="story-title">
            <h2>{story.title}</h2>

            <div className="story-background markdown-content">
              <ReactMarkdown
                remarkPlugins={[remarkGfm, remarkMath]}
                rehypePlugins={[rehypeKatex]}
              >
                {story.background || ""}
              </ReactMarkdown>
            </div>
          </div>

          {story.pages?.map((page) => (
            <div key={page.page_number} className="story-page">
              {page.choice_text && (
                <div className="story-choice">
                  <strong></strong> {page.choice_text}
                </div>
              )}

              <div className="story-content markdown-content">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm, remarkMath]}
                  rehypePlugins={[rehypeKatex]}
                >
                  {page.content || ""}
                </ReactMarkdown>
              </div>
            </div>
          ))}
        </>
      )}
    </div>

    <div className="input-area">
          <textarea
            ref={textareaRef}
            placeholder={
              isExpired ? "This story has expired." : "You can put task generation request here"
            }
            value={inputText}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            disabled={isSending || isExpired}
            rows={1} // Start with a single line
          />

          <button
            onClick={() => handleSubmit(inputText)}
            disabled={isSending || isExpired || !inputText.trim()}
          >
            {isExpired ? 'Expired' : isSending ? 'Sending...' : 'Send'}
          </button>
        </div>
      </>
  </div>
  );
}
