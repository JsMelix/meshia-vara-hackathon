#![cfg_attr(not(feature = "std"), no_std)]

use ink_lang as ink;
use ink_storage::Mapping;
use scale_info::prelude::string::String;
use ink_primitives::AccountId;

#[ink::contract]
mod vara_quiz_contract {
    /// Define la estructura de una pregunta
    #[derive(scale::Encode, scale::Decode, Clone, Default, scale_info::TypeInfo)]
    pub struct Question {
        text: String,
        correct_answer: String,
    }

    /// Define el almacenamiento del contrato
    #[ink(storage)]
    pub struct VaraQuizContract {
        correct_answers: Mapping<AccountId, bool>,
        token_balance: Mapping<AccountId, u32>,
        questions: Mapping<u32, Question>,
        next_question_id: u32,
    }

    impl VaraQuizContract {
        /// Constructor que inicializa el contrato del quiz
        #[ink(constructor)]
        pub fn new() -> Self {
            Self {
                correct_answers: Mapping::default(),
                token_balance: Mapping::default(),
                questions: Mapping::default(),
                next_question_id: 0,
            }
        }

        /// Agrega una nueva pregunta al quiz
        #[ink(message)]
        pub fn add_question(&mut self, text: String, correct_answer: String) {
            let question = Question { text, correct_answer };
            self.questions.insert(self.next_question_id, &question);
            self.next_question_id += 1;
        }

        /// Envía una respuesta a una pregunta
        #[ink(message)]
        pub fn submit_answer(&mut self, question_id: u32, answer: String) -> bool {
            let caller = self.env().caller();
            if let Some(question) = self.questions.get(&question_id) {
                let is_correct = answer == question.correct_answer;
                self.correct_answers.insert(caller, &is_correct);
                if is_correct {
                    let mut balance = self.token_balance.get(&caller).unwrap_or(0);
                    balance += 10; // Recompensa con 10 tokens por respuesta correcta
                    self.token_balance.insert(caller, &balance);
                }
                is_correct
            } else {
                false
            }
        }

        /// Obtiene el balance de tokens del llamante
        #[ink(message)]
        pub fn get_balance(&self) -> u32 {
            self.token_balance.get(&self.env().caller()).unwrap_or(0)
        }

        /// Obtiene una pregunta por su ID
        #[ink(message)]
        pub fn get_question(&self, question_id: u32) -> Option<String> {
            self.questions.get(&question_id).map(|q| q.text.clone())
        }

        /// Elimina una pregunta (para administrador)
        #[ink(message)]
        pub fn delete_question(&mut self, question_id: u32) -> bool {
            self.questions.take(&question_id).is_some()
        }
    }

    #[cfg(test)]
    mod tests {
        use super::*;
        use ink_lang as ink;

        #[ink::test]
        fn test_add_question() {
            let mut contract = VaraQuizContract::new();
            contract.add_question("What is 5 + 5?".to_string(), "10".to_string());
            assert_eq!(contract.next_question_id, 1);
        }

        #[ink::test]
        fn test_submit_answer_correct() {
            let mut contract = VaraQuizContract::new();
            contract.add_question("What is 5 + 5?".to_string(), "10".to_string());
            let caller = ink::env::test::default_accounts::<ink::env::DefaultEnv>().alice;
            ink::env::test::set_caller::<ink::env::DefaultEnv>(caller);
            assert_eq!(contract.submit_answer(0, "10".to_string()), true);
            assert_eq!(contract.get_balance(), 10);
        }

        #[ink::test]
        fn test_submit_answer_incorrect() {
            let mut contract = VaraQuizContract::new();
            contract.add_question("What is 5 + 5?".to_string(), "10".to_string());
            let caller = ink::env::test::default_accounts::<ink::env::DefaultEnv>().alice;
            ink::env::test::set_caller::<ink::env::DefaultEnv>(caller);
            assert_eq!(contract.submit_answer(0, "11".to_string()), false);
            assert_eq!(contract.get_balance(), 0);
        }
    }
}
