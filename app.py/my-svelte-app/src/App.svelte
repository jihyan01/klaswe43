<script>
  import Feed from './src/components/Feed.svelte';
  import { onMount } from 'svelte';

  let question = '';
  let messages = [
    {
      role: "assistant",
      author: "AI",
      text: "안녕하세요! 질문이 있으신가요?",
      isLoading: false,
    }
  ];
  let loading = false;

  // 메시지 전송 핸들러
  const handleSubmit = async () => {
    if (loading || !question) return;
    const tempQuestion = question;
    question = '';

    // 메시지 추가
    messages = messages.concat([
      { role: "user", author: "User", text: tempQuestion, isLoading: false },
      { role: "assistant", author: "AI", text: '', isLoading: true }
    ]);

    loading = true;

    try {
      const formData = new FormData();
      formData.append('question', tempQuestion);

      const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();

      messages.pop();
      messages = messages.concat([
        { role: "assistant", author: "AI", text: data.answer, isLoading: false }
      ]);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      loading = false;
    }
  };
</script>

<div class="ui main text container">
  <div class="ui feed segment scrolling">
    {#each messages as message}
      <Feed {message} />
    {/each}
  </div>
  <form class="ui form" on:submit|preventDefault={handleSubmit}>
    <div class="field">
      <textarea rows="2" bind:value={question} placeholder="질문을 입력하세요"></textarea>
    </div>
    <button class="ui labeled submit icon button" type="submit" disabled: {loading}>
      <i class="icon edit"></i> Send Message
    </button>
  </form>
</div>
