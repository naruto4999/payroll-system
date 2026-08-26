import ReactModal from 'react-modal';

ReactModal.setAppElement('#root');

const maxWidthClasses = {
	sm: 'sm:max-w-sm',
	md: 'sm:max-w-md',
	lg: 'sm:max-w-lg',
	xl: 'sm:max-w-xl',
	'2xl': 'sm:max-w-2xl',
	'3xl': 'sm:max-w-3xl',
};

const Modal = ({ isOpen, onClose, children, className = '', closeOnOverlayClick = true, maxWidth = '3xl' }) => (
	<ReactModal
		isOpen={isOpen}
		onRequestClose={closeOnOverlayClick ? onClose : undefined}
		shouldCloseOnOverlayClick={closeOnOverlayClick}
		shouldCloseOnEsc={closeOnOverlayClick}
		className={`scrollbar mx-2 my-auto max-h-[calc(100dvh-1rem)] overflow-y-auto overscroll-contain rounded-xl bg-white p-0 text-zinc-900 shadow-2xl outline-none dark:bg-zinc-800 dark:text-zinc-100 sm:mx-auto ${maxWidthClasses[maxWidth] || maxWidthClasses['3xl']} ${className}`}
		overlayClassName="fixed inset-0 z-50 flex overflow-hidden bg-zinc-950/60 p-2 backdrop-blur-[2px]"
		contentLabel="Dialog"
	>
		{children}
	</ReactModal>
);

export default Modal;
