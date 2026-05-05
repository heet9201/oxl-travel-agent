# Session Notes: Building a Real AI Agent: From Business Problem to Deployment

**Speaker Notes & Speech Outline**

---

## 1. Introduction (2-3 mins)
* **Hook:** Start with a relatable problem. "How many of you have spent hours juggling between 10 tabs just to plan a simple 3-day trip?"
* **Context:** Today, we are moving beyond simple chatbots. We are building **Agents**—systems that understand context, classify intents, and route tasks to specialized functions.
* **Goal for the Session:** I will walk you through how I built "OXL Travel Agent," a real-world AI travel assistant, from a mere business problem all the way to a fully deployed application.

---

## 2. Identifying the Business Problem (5 mins)
* **The Problem:** Travel planning is fragmented. Users have to check flights, compare hotel prices, estimate budgets, and build itineraries using completely different tools. It’s manual, time-consuming, and overwhelming.
* **Why AI is the Solution:** AI excels at aggregating information and reasoning. Instead of forcing a user to fill out 20 forms, an AI agent can have a natural conversation, extract the required parameters (destination, dates, budget), and do the heavy lifting in the background.

---

## 3. Designing and Structuring the AI Agent (10 mins)
* **Agent Architecture:** Explain that we didn't just use a single prompt. We built an **Orchestrator Pattern**.
* **Inputs & Outputs:** 
  * *Input:* Natural language from the user (e.g., "Plan a 3-day trip to Goa under $500").
  * *Logic:* The Orchestrator agent classifies the intent (is this about flights? hotels? budget?) and extracts entities (Goa, 3 days, $500).
  * *Output:* It then routes the request to a specialized sub-agent (like the Flight Agent or Budget Agent) which returns structured JSON data back to the frontend.
* **Why this matters:** It breaks down complex tasks into manageable, deterministic API calls, making the AI reliable rather than unpredictable.

---

## 4. Building and Integrating the Workflow (10 mins)
* **Tech Stack Overview:** 
  * *Frontend:* Next.js (React) for a fast, dynamic user interface.
  * *Backend:* Python with FastAPI for high-performance API routing.
* **The Integration:** Discuss how the Next.js frontend seamlessly communicates with the FastAPI backend. Emphasize the importance of maintaining conversation history so the agent "remembers" the context of the trip.
* **Handling Real-World Hiccups (Optimization):** 
  * Talk about latency. Initially, using standard API calls took upwards of 20 seconds. 
  * *The Fix:* We optimized this by integrating **Groq** and **NVIDIA NIM** (specifically Llama 3 models) using OpenAI-compatible SDKs. We also built a robust **Fallback Mechanism**. If one model hits a rate limit, the system instantly and invisibly falls back to the next model. *Result: Latency dropped to just 1.6 seconds!*

---

## 5. Deployment: Making it Accessible (10 mins)
* **The Local vs. Production Reality:** 
  * *Current State:* "Right now, as developers, we are used to spinning this up on `localhost` with `npm run dev` and `uvicorn`." 
  * *The Goal:* How do we share this with the world efficiently?
* **The Deployment Strategy:** 
  * We utilized **Docker** to containerize the application. 
  * Instead of paying for two separate servers (one for frontend, one for backend), we used a unified single-container approach. 
  * Inside one Docker container, we run FastAPI in the background and Next.js in the foreground, using Next.js `rewrites` to seamlessly proxy `/api` requests locally.
  * **Render Deployment:** We deployed this containerized application to **Render**. It handles the port bindings dynamically and scales effortlessly.

---

## 6. Evaluating Impact & Scaling (5 mins)
* **Improving Efficiency:** By using an LLM to parse intents, we replaced complex UI forms with a simple chat box.
* **Reducing Manual Effort:** A task that took a user 45 minutes (researching flights, hotels, and daily plans) is now accomplished in under 2 seconds.
* **Scaling:** Because our backend logic is modular (the Orchestrator pattern), if we want to add a "Restaurant Agent" tomorrow, we simply plug it into the orchestrator without rewriting the whole system. 

---

## 7. Conclusion & Q&A (5 mins)
* **Key Takeaway:** Building AI agents isn't just about API calls; it's about structuring data flow, optimizing for latency, and deploying robustly.
* **Call to Action:** Encourage the audience to think of one manual, multi-step process in their own business that could be solved using an Orchestrator Agent.
* **Open the floor for questions.**

---

### *Self-Preparation Checklist before the Session:*
- [ ] Ensure your local environment is running perfectly (`npm run dev` and `uvicorn`).
- [ ] Have the Groq/NVIDIA latency comparison ready as a talking point (it's a great "wow" factor).
- [ ] Be prepared to briefly explain the Dockerfile structure if asked during Q&A (how both Node and Python exist in the same slim image).
