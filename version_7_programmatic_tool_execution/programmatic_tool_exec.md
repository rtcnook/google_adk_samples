# Programmatic Tool Execution in Model Context Protocol (MCP)

This concept refers to an advanced pattern where the AI Agent, instead of calling tools one-by-one (Direct Tool Calling), writes a script (code) to execute multiple tools, process their data, and perform logic in a single execution step.

## Visual Comparison

```mermaid
flowchart LR
    %% GLOBAL STYLES
    classDef actor fill:#f9f,stroke:#333,stroke-width:2px,color:black;
    classDef process fill:#d1e7dd,stroke:#333,stroke-width:1px,color:black;
    classDef tool fill:#fff3cd,stroke:#333,stroke-width:1px,color:black;
    classDef script fill:#e2e3e5,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5,color:black;
    classDef titleBox fill:#fff,stroke:none,font-size:16px,font-weight:bold,color:black;

    %% ==========================================
    %% OPTION A: LEFT SIDE (Direct Calling)
    %% ==========================================
    subgraph Left_Container [ ]
        direction TB
        TitleA("Option A:<br/>Without Programmatic Execution<br/>(Standard Loop)"):::titleBox
        
        subgraph Direct_Calling [Sequence]
            direction TB
            UserA((User)):::actor -->|Prompt| LLM_A[LLM Agent]:::process
            
            LLM_A -->|1. Request Tool A| HostA[MCP Client]:::process
            HostA -->|2. Call API| ToolA["Tool A<br/>(e.g., List Files)"]:::tool
            ToolA -->|3. Return Data| HostA
            HostA -->|4. Return Result| LLM_A
            
            LLM_A -->|5. Request Tool B| HostA
            HostA -->|6. Call API| ToolB["Tool B<br/>(e.g., Read File)"]:::tool
            ToolB -->|7. Return Data| HostA
            HostA -->|8. Return Result| LLM_A
            
            LLM_A -->|9. Final Answer| UserA
        end
        TitleA ~~~ Direct_Calling
    end

    %% INVISIBLE SPACER TO FORCE SEPARATION
    Left_Container ~~~ Right_Container

    %% ==========================================
    %% OPTION B: RIGHT SIDE (Programmatic)
    %% ==========================================
    subgraph Right_Container [ ]
        direction TB
        TitleB("Option B:<br/>With Programmatic Execution<br/>(Code Mode)"):::titleBox

        subgraph Programmatic [Sequence]
            direction TB
            UserB((User)):::actor -->|Prompt| LLM_B[LLM Agent]:::process

            %% Step 1: LLM sends code to Sandbox
            LLM_B -->|1. Write Code Script| Sandbox["Sandbox Environment"]:::process
            
            %% Step 2: Sandbox runs the script
            Sandbox -->|2. Execute Script| Script_Block
            
            subgraph Script_Block ["Inside the Script (Python/JS)"]
                direction TB
                Script(Generated Code):::script
                
                %% Step 3 & 4: Script interacts with Tool A
                Script -->|3. Call Tool A| ToolA_P[Tool A]:::tool
                ToolA_P -->|4. Return Data| Script

                %% Step 5 & 6: Script interacts with Tool B
                Script -->|5. Call Tool B| ToolB_P[Tool B]:::tool
                ToolB_P -->|6. Return Data| Script
            end

            %% Step 7: Sandbox returns final result
            Sandbox -->|7. Return Final Result| LLM_B

            %% Step 8: LLM answers user
            LLM_B -->|8. Final Answer| UserB
        end
        TitleB ~~~ Programmatic
    end