An AI powered simple script that leverages crontab and agentic LLM tooling to send me a regular focused weekly email round up of articles with a small summary of each and a link to view more, to my work email address of stephen.z.phillips@sparktsl.com maybe a dozen articles ,highlighting new developments in AI tooling that might be of interest to me as a developer to investigate and use for building our systems. Things such as comet browser, openai operator, browserOS with MCP, right through to new server side CLI pair programming tools such as OpenCode, Amazon Q, Gemini CLI, and also news about models for such tools like Open AI recently releasing 5.1, Gemini moving to use v3 in it's assistant and also how the new nano banana pro supports combining up to 6 images into one, Opus's performance etc?

It should gather a dozen recent articles about news articles from various sources about AI tools and technologies that will be interesting for a developer like me, including for example things such as tools like Comet Browser, OpenAI operator, BrowserOS with MCP, OpenCode, Amazon Q, Gemini CLI, model updates like OpenAI’s 5.1, Gemini v3 integration, Nano Banana Pro, Opus performance, and similar that an AI developer would find interesting to be kept aware of. It should then prepare a weekly email with short summaries and links for me based on those articles.

We have tools locally here of Perplexica (http://10.0.10.46:3030/discover) and SEARXNG (http://10.0.10.46:4040) that can be leveraged to support this. 

An example of the email content as a suggestion is shown below;
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Weekly AI Tooling Roundup</title>
  </head>
  <body style="margin:0; padding:0; background:#f6f7f9; font-family: Arial, Helvetica, sans-serif; color:#111827;">
    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="background:#f6f7f9; padding:24px 0;">
      <tr>
        <td align="center">
          <!-- Container -->
          <table role="presentation" cellpadding="0" cellspacing="0" width="680" style="width:680px; max-width:100%; background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 2px 10px rgba(0,0,0,0.06);">
            <!-- Header -->
            <tr>
              <td style="padding:22px 26px; background:#0b1020;">
                <div style="font-size:20px; font-weight:700; color:#ffffff; line-height:1.3;">
                  Weekly AI Tooling Roundup
                </div>
                <div style="font-size:13px; color:#cbd5e1; margin-top:4px;">
                  Notable developments through 26 Nov 2025
                </div>
              </td>
            </tr>

            <!-- Intro -->
            <tr>
              <td style="padding:22px 26px;">
                <p style="margin:0 0 12px 0; font-size:15px; line-height:1.6;">
                  Hi Stephen,
                </p>
                <p style="margin:0; font-size:15px; line-height:1.6;">
                  Here’s your weekly rundown of notable AI-tooling developments. These updates cover
                  new browser-based agents, terminal tools for pair programming, and model releases
                  that change how these tools behave. Click the links to dive deeper:
                </p>
              </td>
            </tr>

            <!-- Items -->
            <tr>
              <td style="padding:0 18px 18px 18px;">
                <table role="presentation" cellpadding="0" cellspacing="0" width="100%">

                  <!-- Item 1 -->
                  <tr>
                    <td style="padding:12px 8px; border-top:1px solid #eef2f7;">
                      <div style="font-size:16px; font-weight:700; margin-bottom:6px;">
                        1. Comet browser – Perplexity’s AI-first browser
                      </div>
                      <div style="font-size:14px; line-height:1.6; color:#374151;">
                        Invite-only preview where an assistant panel can summarize emails,
                        suggest calendar adjustments, and extract key data from dense sites.
                        Early testers say it shines for triage and doc review but still
                        hallucinates on high-context tasks.
                      </div>
                      <div style="margin-top:8px;">
                        <a href="https://www.beam.ai/blog/ai-browsers-comet-diatron-openai-operator"
                           style="font-size:14px; color:#2563eb; text-decoration:none;">
                          Read more →
                        </a>
                      </div>
                    </td>
                  </tr>

                  <!-- Item 2 -->
                  <tr>
                    <td style="padding:12px 8px; border-top:1px solid #eef2f7;">
                      <div style="font-size:16px; font-weight:700; margin-bottom:6px;">
                        2. BrowserOS – MCP-driven, privacy-focused agentic browser
                      </div>
                      <div style="font-size:14px; line-height:1.6; color:#374151;">
                        Open-source browser that turns natural-language commands into actions
                        across Gmail, Calendar, Docs, Notion, etc., via built-in MCP servers.
                        Recent releases added an embedded MCP server (no extra install) and
                        improved text extraction for LLM chat.
                      </div>
                      <div style="margin-top:8px;">
                        <a href="https://browseros.com/"
                           style="font-size:14px; color:#2563eb; text-decoration:none;">
                          Project site →
                        </a>
                        <span style="color:#9ca3af; font-size:14px;"> · </span>
                        <a href="https://github.com/state-spaces/browseros/releases"
                           style="font-size:14px; color:#2563eb; text-decoration:none;">
                          Release notes →
                        </a>
                      </div>
                    </td>
                  </tr>

                  <!-- Item 3 -->
                  <tr>
                    <td style="padding:12px 8px; border-top:1px solid #eef2f7;">
                      <div style="font-size:16px; font-weight:700; margin-bottom:6px;">
                        3. OpenAI Operator – autonomous web “computer use” agent
                      </div>
                      <div style="font-size:14px; line-height:1.6; color:#374151;">
                        Research preview agent using GPT-4o + RL to click, type, and navigate
                        websites. Can fill forms, book groceries, and complete multi-step tasks,
                        handing control back to users when needed. Planned to roll into ChatGPT.
                      </div>
                      <div style="margin-top:8px;">
                        <a href="https://openai.com/blog/operator"
                           style="font-size:14px; color:#2563eb; text-decoration:none;">
                          Read more →
                        </a>
                      </div>
                    </td>
                  </tr>

                  <!-- Item 4 -->
                  <tr>
                    <td style="padding:12px 8px; border-top:1px solid #eef2f7;">
                      <div style="font-size:16px; font-weight:700; margin-bottom:6px;">
                        4. Operator in context (eWeek)
                      </div>
                      <div style="font-size:14px; line-height:1.6; color:#374151;">
                        Coverage framing Operator as the move from “answering” to “doing”:
                        autonomous execution across browsing, coding, and task completion,
                        with 2025 positioned as the mainstream year for agentic systems.
                      </div>
                      <div style="margin-top:8px;">
                        <a href="https://www.eweek.com/artificial-intelligence/openai-operator-agent/"
                           style="font-size:14px; color:#2563eb; text-decoration:none;">
                          Read more →
                        </a>
                      </div>
                    </td>
                  </tr>

                  <!-- Item 5 -->
                  <tr>
                    <td style="padding:12px 8px; border-top:1px solid #eef2f7;">
                      <div style="font-size:16px; font-weight:700; margin-bottom:6px;">
                        5. OpenCode CLI – open-source terminal pair-programmer
                      </div>
                      <div style="font-size:14px; line-height:1.6; color:#374151;">
                        Fast, themeable TUI coding agent with LSP context and support for
                        75+ LLM providers (including local). Multi-session workflows and
                        sharable sessions via URL; strong emphasis on code privacy.
                      </div>
                      <div style="margin-top:8px;">
                        <a href="https://opencode.sh/"
                           style="font-size:14px; color:#2563eb; text-decoration:none;">
                          Project site →
                        </a>
                        <span style="color:#9ca3af; font-size:14px;"> · </span>
                        <a href="https://apidog.com/blog/opencode-cli-guide"
                           style="font-size:14px; color:#2563eb; text-decoration:none;">
                          Deep dive →
                        </a>
                      </div>
                    </td>
                  </tr>

                  <!-- Item 6 -->
                  <tr>
                    <td style="padding:12px 8px; border-top:1px solid #eef2f7;">
                      <div style="font-size:16px; font-weight:700; margin-bottom:6px;">
                        6. Amazon Q CLI – terminal-based coding agent
                      </div>
                      <div style="font-size:14px; line-height:1.6; color:#374151;">
                        Case study shows Q CLI generating data models and app scaffolds from
                        natural language, guided by project “rules” files. Lets you inspect
                        and edit context (/context show). A working app outline emerges fast.
                      </div>
                      <div style="margin-top:8px;">
                        <a href="https://dev.to/aconz/using-amazon-q-cli-to-build-a-book-sharing-app"
                           style="font-size:14px; color:#2563eb; text-decoration:none;">
                          Read more →
                        </a>
                      </div>
                    </td>
                  </tr>

                  <!-- Item 7 -->
                  <tr>
                    <td style="padding:12px 8px; border-top:1px solid #eef2f7;">
                      <div style="font-size:16px; font-weight:700; margin-bottom:6px;">
                        7. Gemini CLI + Gemini 3 Pro integration
                      </div>
                      <div style="font-size:14px; line-height:1.6; color:#374151;">
                        Open-source terminal tool with generous free tier and built-in
                        grounding/tools (Search, file ops, shell, fetch). Now upgraded to
                        Gemini 3 Pro for stronger reasoning and agentic coding, including
                        end-to-end project scaffolds and multimodal workflows.
                      </div>
                      <div style="margin-top:8px;">
                        <a href="https://github.com/GoogleCloudPlatform/gemini-code-cli"
                           style="font-size:14px; color:#2563eb; text-decoration:none;">
                          GitHub →
                        </a>
                        <span style="color:#9ca3af; font-size:14px;"> · </span>
                        <a href="https://developers.googleblog.com/2025/11/gemini-3-pro-gemini-cli.html"
                           style="font-size:14px; color:#2563eb; text-decoration:none;">
                          Gemini 3 Pro update →
                        </a>
                      </div>
                    </td>
                  </tr>

                  <!-- Item 8 -->
                  <tr>
                    <td style="padding:12px 8px; border-top:1px solid #eef2f7;">
                      <div style="font-size:16px; font-weight:700; margin-bottom:6px;">
                        8. GPT-5.1 release – Instant + Thinking models
                      </div>
                      <div style="font-size:14px; line-height:1.6; color:#374151;">
                        Adaptive reasoning with two modes: Instant for speed and Thinking
                        for depth. Improves instruction-following, math, and coding; adds
                        better steerability, prompt caching, and more reliable code-edit tools.
                      </div>
                      <div style="margin-top:8px;">
                        <a href="https://openai.com/gpt-5-1"
                           style="font-size:14px; color:#2563eb; text-decoration:none;">
                          Release notes →
                        </a>
                        <span style="color:#9ca3af; font-size:14px;"> · </span>
                        <a href="https://openai.com/developers/gpt-5-1"
                           style="font-size:14px; color:#2563eb; text-decoration:none;">
                          Dev blog →
                        </a>
                      </div>
                    </td>
                  </tr>

                  <!-- Item 9 -->
                  <tr>
                    <td style="padding:12px 8px; border-top:1px solid #eef2f7;">
                      <div style="font-size:16px; font-weight:700; margin-bottom:6px;">
                        9. Gemini 3 + Gemini Agent rollout (Reuters)
                      </div>
                      <div style="font-size:14px; line-height:1.6; color:#374151;">
                        Google ships Gemini 3 directly into Search on day one.
                        “Gemini Agent” handles multi-step tasks (inbox, travel),
                        and new Antigravity platform targets autonomous software dev.
                      </div>
                      <div style="margin-top:8px;">
                        <a href="https://www.reuters.com/technology/google-launches-gemini-3-agent-2025-11-18/"
                           style="font-size:14px; color:#2563eb; text-decoration:none;">
                          Read more →
                        </a>
                      </div>
                    </td>
                  </tr>

                  <!-- Item 10 -->
                  <tr>
                    <td style="padding:12px 8px; border-top:1px solid #eef2f7;">
                      <div style="font-size:16px; font-weight:700; margin-bottom:6px;">
                        10. Nano Banana Pro (Gemini 3 Pro Image)
                      </div>
                      <div style="font-size:14px; line-height:1.6; color:#374151;">
                        Multi-image composition upgrade: up to 14 reference images per generation,
                        keeping up to five people consistent. Supports high-fidelity objects,
                        4K outputs, strong multilingual text rendering, and search-grounded generation.
                      </div>
                      <div style="margin-top:8px;">
                        <a href="https://globalgpt.com/nano-banana-pro-gemini3"
                           style="font-size:14px; color:#2563eb; text-decoration:none;">
                          Read more →
                        </a>
                      </div>
                    </td>
                  </tr>

                  <!-- Item 11 -->
                  <tr>
                    <td style="padding:12px 8px; border-top:1px solid #eef2f7;">
                      <div style="font-size:16px; font-weight:700; margin-bottom:6px;">
                        11. Claude Opus 4.5 – coding/agent performance jump
                      </div>
                      <div style="font-size:14px; line-height:1.6; color:#374151;">
                        Anthropic’s newest Opus model targets long-horizon coding and agentic workflows.
                        Reports substantial reductions in tool-calling and lint/build errors,
                        plus better terminal task performance, at more accessible pricing.
                      </div>
                      <div style="margin-top:8px;">
                        <a href="https://www.anthropic.com/news/claude-opus-4-5"
                           style="font-size:14px; color:#2563eb; text-decoration:none;">
                          Read more →
                        </a>
                      </div>
                    </td>
                  </tr>

                </table>
              </td>
            </tr>

            <!-- Footer -->
            <tr>
              <td style="padding:18px 26px; background:#f9fafb; border-top:1px solid #eef2f7;">
                <p style="margin:0 0 6px 0; font-size:14px; line-height:1.6; color:#374151;">
                  This is an automated email, to unsubscribe click <a href="mailto:stephen.z.phillips@sparktsl.com?subject=unsubAIemail">here</a>
                </p>
                <p style="margin:0; font-size:13px; color:#6b7280;">
                  Happy coding! 🚀
                </p>
              </td>
            </tr>

          </table>
          <!-- /Container -->
        </td>
      </tr>
    </table>
  </body>
</html>
