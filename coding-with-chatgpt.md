# Coding with ChatGPT

I'm not gonna lie - 100% of the code and documentation in this repository were written by ChatGPT-4. Every minor change was made through AI prompting, copy & paste. In this post, I'll walk you through the process.

I usually don't share these internal tools. It's less due to the lack of "open-sourceness" than the extra effort for a proper community release and documentation.

Initially, I planned to track every prompt I used, but the real process is a bit more convoluted than write-requirements-get-the-code. So, it's challenging to present the complete prompts used without further editing of the back-and-forth chat.

The process is pretty much just [putting together some prompts and source files](#the-putting-together-of-some-prompts-and-source-files), like:

- [An initial personality description](#the-personality-description),
- [The code of the source files](#the-source-file),
- Usually the personality description again,
- [The implementation requirements](#the-implementation-requirements), and
- [The expected output format](#the-expected-output-format).

Then, stop ChatGPT whenever it goes off track.
After some cycles and carefully reading through the responses, we should get some decent code change blocks ready to be pasted.

Here are some examples and lessons I learned in this process.
<br><br>

## <a  id="the-putting-together-of-some-prompts-and-source-files"></a>The putting together of some prompts and source files

<img align="right" src="https://user-images.githubusercontent.com/1922654/236931275-f5d001a5-8b5a-4e70-8dc5-0b7960f0fbe5.jpeg"
alt="Mobile screenshot of a Google Spreedsheets with various colors and text walls"
width="250px">

I'm a simple guy with simple tools. I often work on my mobile phone, especially when I have to rock one of my twins, so keeping everything on the same screen, copy and paste ready, is crucial.
Since the whole repo consists of only two Python files and one markdown readme, I used Google Spreadsheet to write the prompt parts and =IMPORTDATA("GitHub/raw/file") to put the source files in individual cells.
So each part of the prompt and source file goes in a cell, one below the other, in a single sheet column. In the next columns, I put small variations in the prompts as the process keeps maturing.
I'm really hoping for better tools sometime soon. At the time of writing, I didn't have access to the GPT-4 model through API, so this entire process took place using the OpenAI chat interface.
<br><br>

## <a  id="the-personality-description">The personality description

Usually, the personality description goes at the beginning of the chat, but in order to be effective, it should be repeated close to the end of the initial message due to context degradation. Here's the description I went with:
You are an AI assistant who specializes in coding, LLMs, ChatGPT, and digital media products. As a highly skilled, sophisticated and creative programmer with over a decade of coding experience, your concise, pedagogical code is so well-structured that comments are rendered redundant due to the clarity of variable and function names. You are helpful, creative, clever, and also incredibly friendly.
<br><br>

## <a  id="the-source-file">The source file

As I mentioned, I used the IMPORTDATA function with some small tweaks to keep the content in a single cell (as opposed to being split in the subsequent cells). Here is the formula:
`=ARRAYFORMULA(JOIN(CHAR(10),SPLIT(IMPORTDATA("https://raw.githubusercontent.com/caetanominuzzo/instruction-induction-optimization/main/main.py")&CHAR(10),CHAR(10))))`

> Remember to force refresh the content of those cells after pushing the changes. To do so, I just delete the cell then undo. BUT, if you have those columns with variations I suggested, you will have to delete everyone in order to refresh. I delete the entire row, supposing all references to the same file are in the same row, then undo. It automatically refreshes in one hour.

It's essential to properly isolate each prompt part, but especially the source files. Remember, we will be copying the entire column to paste in the chat. In fact, every file is represented in three cells. The first cell contains the filename, such as "main.py." The second cell contains the formula to import the file content. The third cell contains a separator, which in my case is "---".
<br><br>

## <a  id="the-implementation-requirements">The implementation requirements

Well, you know, everyone's got their own skills. Writing requirements for code changes is a pretty big topic, and writing specifically for LLMs is like a whole different world, and hardly it gets done on the first try.So, write the requirements simply and quickly, see how ChatGPT responds, stop it when it deviates, and then either 1) add a reply with refined instructions, or 2) go back to the sheets and refine the initial requirement.

Here is an example of a requirement that successfully generated the code for some new configuration params. By successful, I mean that I obtained the final code after making only three course adjustments and stopping during the follow-up messages.

`We need to modify the files above to include new parameters at the beginning of the main.py for 'model', 'max token', 'temperature', and 'presence penalty'. The existing values for these fields should serve as default values.`
<br><br>

## <a  id="the-expected-output-format">The expected output format

Lots of things to unpack here. Asking ChatGPT to rewrite the whole file never works as intended. Sometimes the file gets truncated, sometimes it starts just repeating the original file and forgetting to make any changes, and finally, some amazing times it gives a very good collapsed code with just the modified parts showing, so this last behavior is what we are looking for.

<img width="600px" alt="Screnshoot of ChatGPT inverting what goes inside and outsite of the <code> tag" src="https://user-images.githubusercontent.com/1922654/236931913-a83d5d8d-c72f-4728-8265-91611497df50.png"><br>
Where is up?
<br><br>

To quickly read and analyze the results, the prose and code must be easily separated. All code must come in blocks inside triple backticks, or `code` tags, for fast code copy action. This introduces new issues, such as truncating the end of code blocks and having the subsequent message continue with prose inside the code blocks and code outside of them.

Here's the prompt I used:

`Please don't rewrite all the file, but point me out inside triple backticks exactly where and what needs to be changed.`

When ChatGPT stops mid-coding, use "Continue inside new triple backticks" (add "-cin" to your autocorrect for quick access). But be aware, sometimes they will repeat the whole last line, others will continue where it stopped. Be extra careful when working with white space relevant languages like Python.

It's hard to get this working with markdown, as any code block won't be properly escaped in the ChatGPT interface. I tried asking them to use alternative block codes like 3 brackets, but unsuccessfully. So, I ended up having to reformat the whole readme.md file. I'd appreciate any ideas here.
<br><br>

## Conclusion

<img width="600px" alt="Screenshoot of a file showing its changes ready to be commited" src="https://github.com/caetanominuzzo/lt2/assets/1922654/299985d8-5d06-4548-b296-d9660f7b8008"><br>
Well, at least I wrote the commit message...
<br><br>

So, there you have it! After dancing with ChatGPT-4, juggling prompts, source files, and trying to tame this AI Shoggoth, we've reached the end of our journey.

This open-source method serves as a core component of the dataset optimization process used in the [Small Texts Editor](https://labdqnt.com/). While the editor itself is a separate, commercial product, this method showcases a fascinating glimpse into the world of AI-driven text editing.

In the midst of a Cambrian explosion of evolving tools, it's hard to make any definitive statements, but despite the challenges, no other LLM can deliver results like OpenAI GPT-4. Among other closed models, MidJorney, in particular, stands out as a notable example, leaving competitors like StableDifusion in the dust. And even with all the well-deserved hype around HuggingFace and open models, they are miles away from the likes of OpenAI GPT-4 or MidJorney. Let's hope for changes in this direction soon.

For now, just remember: with a little patience, a keen eye for refining prompts, and a lot of stopping and starting, you can maybe even keep your coding job, freed at least from the burden of coding. Cheers!
