"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

const SECRET_CODE = "klaatu";

export function GlobalKeyListener() {
  const router = useRouter();
  const [inputBuffer, setInputBuffer] = useState("");

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Adiciona a tecla ao buffer (apenas letras)
      if (/^[a-zA-Z]$/.test(e.key)) {
        setInputBuffer((prev) => {
          const newBuffer = (prev + e.key.toLowerCase()).slice(-SECRET_CODE.length);
          
          if (newBuffer === SECRET_CODE) {
            console.log("👁️ O VAZIO TE CHAMA...");
            router.push("/dashboard/void");
          }
          
          return newBuffer;
        });
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [router]);

  return null; // Componente invisível
}