# Intelligent Research-Driven Website Builder Agent Flow

## Complete System Architecture

```mermaid
flowchart TD
    USER[User Input: Topic<br/><i>Simple topic input</i>]
    ROOT[root_website_builder<br/><i>Sequential orchestrator</i>]
    
    subgraph PIPELINE [6-Agent Sequential Pipeline]
        direction LR
        QG[questions_generator<br/><i>Creates 5 questions</i>]
        
        subgraph PARALLEL [5-Agent Parallel Research]
            direction TB
            QR1[QuestionResearcher1<br/><i>Researches Q1</i>]
            QR2[QuestionResearcher2<br/><i>Researches Q2</i>]
            QR3[QuestionResearcher3<br/><i>Researches Q3</i>]
            QR4[QuestionResearcher4<br/><i>Researches Q4</i>]
            QR5[QuestionResearcher5<br/><i>Researches Q5</i>]
        end
        
        QGE[query_generator<br/><i>Merges research</i>]
        RW[requirements_writer<br/><i>Creates report specs</i>]
        DES[designer<br/><i>Visual design</i>]
        CW[code_writer<br/><i>Generates HTML</i>]
    end
    
    OUTPUT[Final HTML Output<br/><i>Research report webpage</i>]
    
    USER --> ROOT
    ROOT --> PIPELINE
    QG --> QR1
    QG --> QR2
    QG --> QR3
    QG --> QR4
    QG --> QR5
    QR1 --> QGE
    QR2 --> QGE
    QR3 --> QGE
    QR4 --> QGE
    QR5 --> QGE
    QGE --> RW
    RW --> DES
    DES --> CW
    PIPELINE --> OUTPUT
    
    classDef userStyle fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    classDef orchestratorStyle fill:#f3e5f5,stroke:#4a148c,stroke-width:3px
    classDef agentStyle fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef parallelStyle fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef outputStyle fill:#fce4ec,stroke:#880e4f,stroke-width:3px
    classDef pipelineStyle fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    
    class USER userStyle
    class ROOT orchestratorStyle
    class QG,QGE,RW,DES,CW agentStyle
    class QR1,QR2,QR3,QR4,QR5 parallelStyle
    class OUTPUT outputStyle
    class PIPELINE pipelineStyle
```

## Key Features Illustrated:

### 🎯 **Sequential Orchestration**
- Root agent manages the entire 6-agent pipeline
- Each agent runs in sequence, passing data through state keys

### ⚡ **Parallel Processing** 
- 5 research agents run simultaneously for efficiency
- All research outputs feed into the query generator

### 📊 **Data Flow**
- Dotted lines show how data flows between agents via state keys
- Each agent's output becomes the next agent's input

### 🔄 **Research-Driven Approach**
- Topic → Questions → Research → Synthesis → Requirements → Design → Code
- Every webpage built on comprehensive research foundation

---

## Usage in VS Code:

1. Install **"Mermaid Preview"** extension
2. Open this file in VS Code
3. Use `Ctrl+Shift+P` → "Mermaid Preview: Open Preview to the Side"
4. The diagram will render beautifully with interactive elements