<script>
    import { onMount } from "svelte";
    import headerName from "../store";
    import Feed from "../components/Feed.svelte";
  
    let question = "";
    let loading = false;
    let messages = [
      {
        role: "assistant",
        author: "AI",
        text: "안녕하세요! 질문이 있으신가요?",
        isLoading: false,
      },
    ];
  
    onMount(() => {
      headerName.set("메인화면");
    });
  
    const handleSubmit = async () => {
      if (loading || !question.trim()) {
        alert("빈 질문은 허용되지 않습니다.");
        return;
      }
  
      const tempQuestion = question;
      question = "";
      messages = [
        ...messages,
        { role: "user", author: "User", text: tempQuestion, isLoading: false },
        { role: "assistant", author: "AI", text: "", isLoading: true },
      ];
  
      loading = true;
  
      try {
        const formData = new FormData();
        formData.append("question", tempQuestion);
  
        const payload = new URLSearchParams(formData);
        const response = await fetch("/api/chat", {
          method: "POST",
          body: payload,
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        });
  
        const data = await response.json();
  
        messages = messages.map((msg, index) =>
          index === messages.length - 1
            ? { ...msg, text: data.answer, isLoading: false }
            : msg
        );
      } catch (error) {
        console.error("Error:", error);
        alert("오류가 발생했습니다. 다시 시도해주세요.");
      } finally {
        loading = false;
      }
    };
  </script>
  
  <div class="ui main text container">
    <div class="ui">
      <div class="ui feed segment scrolling">
        {#each messages as message}
          <Feed message={message} />
        {/each}
      </div>
    </div>
    <form class="ui form" on:submit|preventDefault={handleSubmit}>
      <div class="field">
        <textarea
          rows="2"
          bind:value={question}
          placeholder="질문을 입력하세요."
        ></textarea>
      </div>
      <button
        class="ui labeled submit icon button"
        type="submit"
        disabled: {loading}
      >
        <i class="icon edit"></i> Send Message
      </button>
    </form>
  </div>
  