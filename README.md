<p>the Bash Alias Editor terminal GUI</p>
<img width="1265" height="813" alt="bae" src="https://github.com/user-attachments/assets/258b70fc-fe7e-45e7-a223-5b0d8a4dc99d" />
<p>A python script that makes creating new command shortcuts simple</p>
<p>No need to remember the command to edit you bash_aliases file or the format</p> 
<p>Simply type your alias name in the left column and the command you want it to execute in the right column</p>
<p>to install use</p>
<figure>
  <figcaption>Terminal Session</figcaption>
  <pre>
<span class="prompt">user@host:~$</span> <kbd>cd /your_dir_here</kbd>
<span class="prompt">user@host:~$</span> <kbd>git clone https://github.com/geovanielegend/bae</kbd>
<span class="prompt">user@host:~$</span> <kbd>_</kbd>
  </pre>
</figure>
<p>Recommended folder is the ~/ default where terminal starts, I have included a bae.sh that you just need to make executable using</p>
<figure>
  <figcaption>Terminal Session</figcaption>
  <pre>
<span class="prompt">user@host:~$</span> <kbd>sudo chmod +x bae.sh</kbd>
<span class="prompt">user@host:~$</span> <kbd>_</kbd>
  </pre>
</figure>
<p>Once you have both files in place run it using /.bae.sh</p>
<p>NOTICE: This script edits your ~/.bash_aliases and NOT the ~/.bashrc so if your bashrc does not include bash_aliases for shortcuts you will need to include that as the following...</p>
<img width="718" height="177" alt="bashrc" src="https://github.com/user-attachments/assets/77d1d8d6-7698-42c5-a2da-abce933f78e7" />

