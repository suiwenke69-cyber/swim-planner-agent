# 🏊 Swim Planner

**A multimodal, stateful AI swimming planner built with OpenAI, LangChain, LangGraph, Streamlit, and Supabase.**

Swim Planner turns natural-language requests, meal context, meal photos, and recent training history into structured swimming plans.

Rather than asking a single LLM to perform the entire workflow, V2 separates language understanding, nutrition analysis, deterministic planning tools, memory, and response generation into an explicit LangGraph workflow.

### 🌐 Live Demo

**[Try Swim Planner V2](https://swim-planner-agent-ahnq3yqegicktny8qyweht.streamlit.app/)**

> Swim Planner is currently an experimental public beta. Nutrition, meal-timing, and training recommendations are estimates and should not be treated as medical advice.

---

## ✨ What It Does

Swim Planner can:

- Understand natural-language swimming requests
- Generate structured swimming workouts
- Analyze meals from text
- Analyze meal photos using multimodal AI
- Estimate calories and macronutrients
- Estimate pre-swim meal timing
- Record completed swimming sessions
- Maintain persistent training history
- Analyze recent training load
- Adjust requested workout intensity
- Maintain multi-turn conversation state
- Separate conversation memory from long-term user memory

Example:

> I ate this meal 45 minutes ago. I'm a beginner and want a 40-minute moderate aerobic freestyle swim in a 25-meter pool.

With an uploaded meal image, the system can produce:

```text
Meal Image
    ↓
Visual Food Recognition
    ↓
Portion Estimation
    ↓
Calories / Protein / Carbs / Fat / Fiber
    ↓
Meal Timing
    ↓
Recent Training History
    ↓
Training Load
    ↓
Intensity Decision
    ↓
Structured Swimming Workout
```

---

# 🧠 Architecture

V2 is built as a modular agent workflow rather than a single large prompt.

```text
                         USER
                           │
                           ▼
                       Streamlit
                           │
                           ▼
                    LangGraph State
                           │
                           ▼
                      Parse Input
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
       Completed Swim?          Planning Request
                │                     │
                ▼                     ▼
          Save History            Meal Input?
                │              ┌──────┴──────┐
                │              │             │
                │              ▼             ▼
                │        Meal Image       Text Meal
                │              │             │
                │              ▼             ▼
                │      Vision Nutrition   Nutrition
                │              └──────┬──────┘
                │                     ▼
                │                Meal Timing
                │                     │
                │                     ▼
                │               Load History
                │                     │
                │                     ▼
                │               Training Load
                │                     │
                │                     ▼
                │            Intensity Decision
                │                     │
                │                     ▼
                │                  Workout
                │                     │
                └─────────────┬───────┘
                              ▼
                       Final Response
                              │
                              ▼
                             USER
```

The architecture intentionally separates:

- **LLM reasoning and interpretation**
- **Deterministic Python tools**
- **Workflow orchestration**
- **Conversation state**
- **Persistent user memory**

---

# 🔀 Why LangGraph?

Earlier versions of the project handled most logic inside a single agent execution flow.

V2 uses LangGraph to represent the workflow explicitly.

Each node has one primary responsibility:

```text
Parse Input
Nutrition Analysis
Vision Nutrition
Meal Timing
Load History
Training Load
Intensity Decision
Workout Generation
Memory Write
Final Response
```

Conditional edges determine which nodes actually execute.

For example:

```text
Meal image exists
        ↓
Vision Nutrition

Text meal exists
        ↓
Text Nutrition

No meal
        ↓
Skip Nutrition

Completed swim
        ↓
Write Long-Term Memory
```

This makes the workflow easier to inspect, test, extend, and debug than a single monolithic agent function.

---

# 📷 Multimodal Nutrition Analysis

Swim Planner V2 supports both text and image-based meal input.

## Text

Example:

> I ate chicken rice, a fried egg, and milk tea 45 minutes ago.

## Vision

Users can upload a meal photograph directly through the web interface.

The multimodal nutrition component estimates:

- Visible foods
- Approximate portions
- Calories
- Protein
- Carbohydrates
- Fat
- Fiber
- Digestion load
- Confidence
- Sources of uncertainty

Example structured output:

```json
{
  "food_items": [
    {
      "name": "steamed rice",
      "estimated_portion": "about 200–250 g",
      "confidence": "medium"
    },
    {
      "name": "roasted chicken",
      "estimated_portion": "about 120–160 g",
      "confidence": "medium"
    }
  ],
  "calories_kcal": {
    "low": 650,
    "high": 850
  },
  "protein_g": {
    "low": 30,
    "high": 45
  }
}
```

Nutrition values are intentionally represented as **ranges** rather than false-precision point estimates.

The system also explicitly represents uncertainty when portion size, cooking oil, sauces, or preparation methods cannot be determined visually.

---

# 🏊 Structured Workout Planning

Workout generation is separated from the LLM response layer.

The planner produces structured workout objects containing information such as:

- Duration
- Intensity
- Swimming level
- Goal
- Stroke
- Pool length
- Estimated total distance
- Warm-up
- Main set
- Cool-down

This allows the application to use the same workout data for:

- Natural-language responses
- Streamlit dashboards
- Training history
- Future analytics
- Testing

The LLM explains the workout but does not need to recalculate the deterministic tool output.

---

# 🧠 Memory Architecture

V2 deliberately separates two different kinds of memory.

## 1. Conversation Memory

Implemented using:

**LangGraph `InMemorySaver`**

Used for temporary thread-level context such as:

```text
User:
I want a 40-minute moderate freestyle swim.

User:
Actually, make it hard.
```

The second message can inherit information from the first message within the same conversation.

Starting a **New Conversation** creates a new LangGraph thread.

---

## 2. Long-Term Training Memory

Implemented using:

**Supabase PostgreSQL**

Completed swimming sessions are stored independently of conversation threads.

```text
Anonymous User
      │
      ├── Conversation A
      ├── Conversation B
      └── Conversation C
              │
              ▼
        Same User Memory
              │
              ▼
       Supabase PostgreSQL
              │
              ▼
       Swimming History
```

A user can say:

> I just finished a 40-minute hard swim.

The agent detects that the message describes a completed session and writes it to long-term memory.

Future conversations can load that history and use it during workout planning.

---

# 📈 Training Load & Intensity Decisions

Recent swimming history is passed through a deterministic training-load tool.

The current prototype considers factors including:

- Sessions during the last 7 days
- Total swimming minutes
- Easy sessions
- Moderate sessions
- Hard sessions
- Simplified training-load score

The resulting recommendation is compared against the user's requested intensity.

Example:

```text
User request
    ↓
HARD

Recent history
    ↓
2 hard sessions

Training Load
    ↓
EASY recommended

Intensity Decision
    ↓
Requested: HARD
Recommended: EASY
Final: EASY

Workout
    ↓
EASY
```

The system preserves the distinction between:

```text
User Intent
    ↓
Agent Decision
    ↓
Executed Workout
```

rather than overwriting the user's original request.

---

# ⚡ V1 → V2

The project was intentionally developed in multiple generations.

## V1

V1 explored a locally hosted agent architecture using a local Qwen model.

It included:

- Local LLM inference
- Memory
- State extraction
- Python tools
- Workout generation
- Performance instrumentation
- Streamlit interface

A representative V1 benchmark:

```text
Memory analysis:     24.475 s
State extraction:    21.551 s
Python tools:         0.003 s
Final response:      76.336 s
--------------------------------
Total:              122.366 s
```

A later web run was approximately:

```text
Memory:          13.49 s
State:           17.36 s
Python tools:     0.005 s
Response:        89.14 s
--------------------------------
Total:          120.00 s
```

The primary bottleneck was local LLM inference rather than deterministic Python tooling.

---

## V2

V2 moved to:

- OpenAI models
- LangChain structured output
- LangGraph orchestration
- Explicit state
- Conditional routing
- Multimodal vision
- Supabase long-term memory

Representative V2 end-to-end benchmark:

```text
Parse Input:          5.168 s
Nutrition Analysis:  11.695 s
Meal Timing:          <0.001 s
Workout:              <0.001 s
Final Response:       15.172 s
--------------------------------
Total LangGraph:      32.040 s
```

In this run, measured node execution accounted for approximately:

```text
32.035 s
```

of the:

```text
32.040 s
```

total graph execution time.

This indicated negligible orchestration overhead in that benchmark, while LLM inference remained the dominant source of latency.

### Approximate End-to-End Improvement

| Version | Architecture | Representative latency |
|---|---|---:|
| V1 | Local Qwen-based agent | ~120–122 s |
| V2 | OpenAI + LangGraph | ~32 s |

V2 reduced representative end-to-end latency by approximately **73–74%** while adding structured nutrition analysis, multimodal input, explicit workflow orchestration, and cloud-backed memory.

> Benchmarks are development measurements rather than controlled production performance guarantees. API and model latency can vary between requests.

---

# 🛠 Tech Stack

### AI

- OpenAI
- LangChain
- LangGraph
- Structured Pydantic outputs
- Multimodal vision

### Application

- Python
- Streamlit
- Pydantic

### Memory & Data

- Supabase
- PostgreSQL
- LangGraph Checkpointer

### Deployment

- GitHub
- Streamlit Community Cloud

---

# 🗂 Project Structure

```text
swim-planner-agent/
│
├── v1/
│   ├── agent_core.py
│   ├── app.py
│   ├── cli.py
│   ├── memory.py
│   ├── prompts.py
│   ├── state.py
│   └── tools.py
│
├── v2/
│   ├── agent/
│   │   ├── graph.py
│   │   ├── nodes.py
│   │   ├── prompts.py
│   │   └── state.py
│   │
│   ├── memory/
│   │   └── store.py
│   │
│   ├── models/
│   │   ├── nutrition.py
│   │   ├── provider.py
│   │   ├── training.py
│   │   ├── user_input.py
│   │   └── workout.py
│   │
│   └── tools/
│       ├── meal_timing.py
│       ├── nutrition.py
│       ├── training_load.py
│       ├── user_input.py
│       ├── vision_nutrition.py
│       └── workout.py
│
├── tests/
│
├── v2_app.py
├── requirements.txt
└── README.md
```

---

# 🚀 Run Locally

## 1. Clone the repository

```bash
git clone https://github.com/suiwenke69-cyber/swim-planner-agent.git
cd swim-planner-agent
```

## 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Create:

```text
.env
```

Add:

```text
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_server_key
```

Do not commit `.env`.

## 5. Start the application

```bash
streamlit run v2_app.py
```

---

# 🧪 Testing

The repository contains tests covering major components of the V2 architecture, including:

- Structured input parsing
- Nutrition analysis
- Meal timing
- Training history
- Training-load decisions
- LangGraph checkpointing
- Persistent memory
- Duplicate protection
- Cross-user memory isolation
- Supabase connectivity
- Supabase CRUD operations
- Vision nutrition
- Multimodal graph execution
- End-to-end agent execution

Example:

```bash
python -m tests.test_v2_end_to_end
```

---

# 🔐 Privacy & Public Beta Design

The current public beta does not provide user accounts.

Visitors receive an anonymous application identity used to isolate training records.

Long-term swimming history is stored in Supabase and separated by anonymous user ID.

Conversation state and long-term training history are intentionally treated as different systems:

```text
Conversation State
→ LangGraph Checkpointer

Long-Term Training History
→ Supabase PostgreSQL
```

This architecture is designed so that a future authentication layer can replace anonymous identity without requiring the planning workflow to be redesigned.

---

# ⚠️ Current Limitations

Swim Planner V2 is an experimental software project.

### Nutrition

Nutrition estimates from text or images may be inaccurate, particularly when:

- Portion sizes are unclear
- Cooking oil is not visible
- Sauces or ingredients are hidden
- Food preparation cannot be determined from the image

### Meal Timing

The current meal-timing system uses **prototype planning heuristics**.

It has not yet been replaced by a fully evidence-based sports-nutrition model.

### Training Load

The current training-load score is also a simplified prototype heuristic rather than a validated physiological training-load model.

### Anonymous Identity

The public beta does not currently provide account-based authentication.

### AI Output

LLM and vision outputs can be incorrect and should not be treated as medical, nutritional, or professional coaching advice.

---

# 🗺 Roadmap

Planned areas of improvement include:

- Evidence-based pre-exercise meal timing
- Evidence-based training-load modeling
- User authentication
- Stable account-level profiles
- Improved anonymous identity persistence
- More robust duplicate-event detection
- Better portion estimation
- Nutrition database integration
- Cost and rate-limit protection
- Improved mobile UI
- Expanded workout personalization
- Additional swimming performance metrics
- Further latency optimization

---

# 💡 Engineering Takeaways

This project was designed as an exploration of how an AI application evolves from a simple LLM prototype into a structured agent system.

Several architectural principles emerged during development:

### LLMs are useful for interpretation

Natural-language understanding, food recognition, uncertain nutrition estimation, and user-facing explanation benefit from model reasoning.

### Deterministic logic belongs in tools

Calculations and explicit planning rules are easier to test and control when implemented as Python functions.

### State is not the same as memory

Conversation state and long-term user history have different lifecycles and should be modeled separately.

### Uncertainty should be represented explicitly

When the system lacks sufficient information, returning no recommendation or a confidence range is preferable to inventing false precision.

### Interfaces matter

Because text nutrition and vision nutrition return the same structured `MealAnalysis` object, the rest of the planning workflow does not need to care where the information came from.

---

# 🌐 Live Demo

### **[Launch Swim Planner V2 →](https://swim-planner-agent-ahnq3yqegicktny8qyweht.streamlit.app/)**

---

## Disclaimer

Swim Planner is an experimental AI software project.

Nutrition estimates, meal-timing suggestions, training-load calculations, and workout recommendations are provided for demonstration and planning purposes only and are **not medical advice, nutritional advice, or a substitute for professional coaching**.